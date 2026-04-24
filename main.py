import re
import sys
import os
import time
import io
import random
import contextlib
import inquirer
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from rich.table import Table
from core.engine import Engine

if sys.platform == "win32":
    os.system("")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

console = Console(highlight=False)

A  = "#00e5ff"   # electric cyan - prompts / accents
V  = "#7c3aed"   # deep violet - banner top
MV = "#b388ff"   # soft violet - banner mid
OK = "#69ff47"   # neon lime - success
ER = "#ff4d4d"   # neon red - errors
DM = "#546e7a"   # blue-grey - dim / meta
KY = "#80deea"   # light teal - table keys
VL = "#cfd8dc"   # off-white - table values
HL = "#ffd740"   # amber - counts / highlights

VERSION = "v1.1.0"
_GLITCH  = r"!@#$%^&*<>[]{}|\/?~`0123456789XZ@#$!"

BANNER = [
    "  ;                                               ;                                           ",
    "  ED.                                             ED.              :                          ",
    "  E#Wi                                          ,;E#Wi            t#,     L.                  ",
    "  E###G.       j.                             f#i E###G.         ;##W.    EW:        ,ft      ",
    "  E#fD#W;      EW,                   ..     .E#t  E#fD#W;       :#L:WE    E##;       t#E      ",
    "  E#t t##L     E##j                 ;W,    i#W,   E#t t##L     .KG  ,#D   E###t      t#E      ",
    "  E#t  .E#K,   E###D.              j##,   L#D.    E#t  .E#K,   EE    ;#f  E#fE#f     t#E      ",
    "  E#t    j##f  E#jG#W;            G###, :K#Wfff;  E#t    j##f f#.     t#i E#t D#G    t#E      ",
    "  E#t    :E#K: E#t t##f         :E####, i##WLLLLt E#t    :E#K::#G     GK  E#t  f#E.  t#E      ",
    "  E#t   t##L   E#t  :K#E:      ;W#DG##,  .E#L     E#t   t##L   ;#L   LW.  E#t   t#K: t#E      ",
    "  E#t .D#W;    E#KDDDD###i    j###DW##,    f#E:   E#t .D#W;     t#f f#:   E#t    ;#W,t#E      ",
    "  E#tiW#G.     E#f,t#Wi,,,   G##i,,G##,     ,WW;  E#tiW#G.       f#D#;    E#t     :K#D#E      ",
    "  E#K##i       E#t  ;#W:   :K#K:   L##,      .D#; E#K##i          G#t     E#t      .E##E      ",
    "  E##D.        DWi   ,KK: ;##D.    L##,        tt E##D.            t      ..         G#E      ",
    "  E#t                     ,,,      .,,            E#t                                 fE      ",
    "  L:                                              L:                                   ,      ",
]

_COLORS = (
    [V]  * 3 +
    [MV] * 5 +
    [A]  * (len(BANNER) - 8)
)

def _glitch_line(line: str, step: int, total: int) -> str:
    noise = 1.0 - step / total
    return "".join(
        " " if ch == " "
        else (random.choice(_GLITCH) if random.random() < noise * 0.82 else ch)
        for ch in line
    )


def _build_banner(step: int | None = None, total: int = 18) -> Text:
    t = Text("\n")
    for i, line in enumerate(BANNER):
        color = _COLORS[min(i, len(_COLORS) - 1)]
        body  = _glitch_line(line, step, total) if (step is not None and step < total) else line
        t.append(body + "\n", style=color)
    return t


def _typewrite(parts: list[tuple[str, str]], delay: float = 0.013) -> None:
    for txt, sty in parts:
        for ch in txt:
            console.print(ch, end="", style=sty, highlight=False)
            try:
                console.file.flush()
            except Exception:
                pass
            time.sleep(delay)
    console.print()

def _banner() -> None:
    total = 18
    with Live(
        _build_banner(0, total),
        console=console,
        refresh_per_second=24,
        transient=False,
    ) as live:
        for step in range(1, total + 1):
            live.update(_build_banner(step, total))
            time.sleep(0.050)
    _typewrite(
        [("\n  I could not ask for a better subject!  ·  ", DM), (VERSION, A)],
        delay=0.020,
    )
    console.print()

def _banner_static() -> None:
    console.print(_build_banner())
    console.print(f"\n  [{DM}]I could not ask for a better subject!  ·  {VERSION}[/{DM}]\n")

def _boot_line(tag: str, label: str, status: str = "OK", animated: bool = True) -> None:
    pad = max(0, 36 - len(label))
    parts: list[tuple[str, str]] = [
        ("  [", DM), (tag, A), ("]  ", DM),
        (label, DM), (" " * pad + "  ", DM),
        (status, OK if status == "OK" else ER),
    ]
    if animated:
        _typewrite(parts, delay=0.007)
    else:
        t = Text()
        for txt, sty in parts:
            t.append(txt, style=sty)
        console.print(t)

def _sep(width: int = 48) -> None:
    console.print(f"  [{DM}]{'-' * width}[/{DM}]")

def identify_target(s: str) -> str:
    s = s.strip()
    if re.match(r"^CVE-\d{4}-\d{4,}$", s, re.IGNORECASE):
        return "cve"
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", s):
        return "ip"
    if re.match(r"^https?://", s, re.IGNORECASE):
        return "url"
    if re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", s):
        return "email"
    if re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9\-]+)+$", s):
        return "domain"
    return "unknown"

def _flat_rows(data: dict) -> list[tuple[str, str, bool]]:
    rows: list[tuple[str, str, bool]] = []
    for key, val in data.items():
        if val is None:
            continue
        if isinstance(val, dict):
            rows.append((key, "", True))
            for sub_k, sub_v in val.items():
                rows.append((f"  {sub_k}", str(sub_v), False))
        elif isinstance(val, list):
            if not val:
                continue
            if len(val) <= 4:
                rows.append((key, "   ".join(str(v) for v in val), False))
            else:
                rows.append((key, f"{len(val)} entries", False))
                for item in val:
                    rows.append(("", str(item), False))
        else:
            rows.append((key, str(val), False))
    return rows

def _print_result(res) -> None:
    if not res.success:
        console.print(f"\n  [{ER}]✗  {res.module_name.upper()}[/{ER}]")
        _sep()
        console.print(f"  [{ER}]{res.error}[/{ER}]\n")
        return

    table = Table(
        title=f"[bold {OK}]✔  {res.module_name.upper()}[/bold {OK}]",
        title_justify="left",
        show_header=True,
        header_style=f"bold {KY}",
        border_style=DM,
        padding=(0, 2),
        min_width=52,
    )
    table.add_column("Property", style=KY, no_wrap=True, min_width=20)
    table.add_column("Value",    style=VL)

    for key, val, is_header in _flat_rows(res.result_data):
        if is_header:
            table.add_row(f"[{HL}]{key}[/{HL}]", "")
        else:
            table.add_row(key, val)

    console.print()
    console.print(table)
    console.print()


def _print_summary(results: list) -> None:
    _sep(48)
    ok_n   = sum(1 for r in results if r.success)
    fail_n = len(results) - ok_n
    t = Text()
    t.append("  scan complete  ·  ", style=DM)
    t.append(f"{ok_n} ok", style=OK)
    t.append("  ·  ", style=DM)
    t.append(f"{fail_n} failed", style=ER if fail_n else DM)
    console.print(t)
    console.print()

def _execute_modules(engine: Engine, modules: list, target: str) -> list:
    results = []
    for mod in modules:
        spin_txt = Text()
        spin_txt.append("  running  ", style=DM)
        spin_txt.append(mod.name, style=KY)
        spin_txt.append("...", style=DM)
        with Live(
            Spinner("dots2", text=spin_txt),
            console=console,
            refresh_per_second=20,
            transient=True,
        ):
            result = mod.run(target)
            engine.storage.save(result)
            results.append(result)
        _print_result(result)
    return results

def _run_autopilot(engine: Engine) -> bool:
    console.print()
    target = console.input(f"  [{A}]--›  target : [/{A}]").strip()
    if not target:
        return False

    ttype = identify_target(target)
    if ttype == "unknown":
        console.print(f"\n  [{ER}]could not detect target type - check your input[/{ER}]\n")
        return False

    info = Text()
    info.append("\n  target    ", style=DM)
    info.append(target, style=A)
    info.append("  ·  type: ", style=DM)
    info.append(ttype, style=HL)
    console.print(info)

    eligible = [m for m in engine.modules.values() if m.can_handle(ttype)]
    if not eligible:
        console.print(f"\n  [{ER}]no modules available for type: {ttype}[/{ER}]\n")
        return False

    console.print(f"  [{DM}]{len(eligible)} module(s) queued[/{DM}]\n")
    results = _execute_modules(engine, eligible, target)
    _print_summary(results)
    return True


def _run_manual(engine: Engine) -> bool:
    console.print()
    choices = [
        (f"{name:<22}[{', '.join(mod.supported_types)}]  -  {mod.description}", name)
        for name, mod in engine.modules.items()
    ]

    try:
        answers = inquirer.prompt([
            inquirer.Checkbox(
                "modules",
                message="Select modules  (Space = toggle  ·  Enter = confirm)",
                choices=choices,
            ),
        ])
    except KeyboardInterrupt:
        return False

    if not answers or not answers["modules"]:
        console.print(f"\n  [{DM}]no modules selected[/{DM}]\n")
        return False

    selected = [engine.modules[n] for n in answers["modules"] if n in engine.modules]

    console.print()
    target = console.input(f"  [{A}]--›  target : [/{A}]").strip()
    if not target:
        return False

    info = Text()
    info.append("\n  target    ", style=DM)
    info.append(target, style=A)
    info.append(f"  ·  {len(selected)} module(s) queued", style=DM)
    console.print(info)
    console.print()

    results = _execute_modules(engine, selected, target)
    _print_summary(results)
    return True

def main() -> None:
    console.clear()
    _banner()

    _boot_line("SYS", "runtime environment")
    time.sleep(0.09)
    _boot_line("NET", "network stack")
    time.sleep(0.09)
    buf = io.StringIO()
    spin_txt = Text()
    spin_txt.append("  [", style=DM)
    spin_txt.append("MOD", style=A)
    spin_txt.append("]  loading modules...", style=DM)

    with Live(
        Spinner("dots2", text=spin_txt),
        console=console,
        refresh_per_second=20,
        transient=True,
    ):
        with contextlib.redirect_stdout(buf):
            engine = Engine()
        time.sleep(0.30)

    loaded = list(engine.modules.values())
    _boot_line("MOD", f"{len(loaded)} modules loaded", animated=False)
    console.print()

    module_line = f"  [{HL}]◈  {len(loaded)} module(s) active[/{HL}]\n"
    console.print(module_line)

    # Main loop
    first_iter = True
    while True:
        if not first_iter:
            console.clear()
            _banner_static()
            console.print(module_line)
        first_iter = False

        try:
            answers = inquirer.prompt([
                inquirer.List(
                    "mode",
                    message="Select mode",
                    choices=[
                        ("  Auto-Pilot       detect type, run all matching modules", "auto"),
                        ("  Manual Override  pick modules, then enter target",        "manual"),
                        ("  Exit", "exit"),
                    ],
                ),
            ])
        except KeyboardInterrupt:
            console.print(f"\n  [{DM}]interrupted[/{DM}]\n")
            return

        if not answers or answers["mode"] == "exit":
            console.print(f"\n  [{DM}]shutting down...[/{DM}]\n")
            return

        ran = (
            _run_autopilot(engine) if answers["mode"] == "auto"
            else _run_manual(engine)
        )

        if ran:
            console.print(
                f"  [bold {OK}]✔[/bold {OK}]  [{DM}]results saved to database[/{DM}]"
            )

        try:
            console.input(f"\n  [{DM}]press Enter to return to main menu...[/{DM}]")
        except (KeyboardInterrupt, EOFError):
            pass


if __name__ == "__main__":
    main()
