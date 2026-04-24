import re
import time
import io
import contextlib
import inquirer
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from rich.table import Table
from core.engine import Engine

console = Console()

A  = "#00e5ff"   # electric cyan  - accents, prompts
V  = "#b388ff"   # soft violet    - banner top
OK = "#69ff47"   # neon lime      - success
ER = "#ff4d4d"   # neon red       - errors
DM = "#546e7a"   # blue-grey      - dim / meta
KY = "#80deea"   # light teal     - keys
VL = "#cfd8dc"   # off-white      - values

BANNER = [
    r" ██████╗ ██████╗  █████╗ ███████╗██████╗  ██████╗ ███╗   ██╗",
    r" ██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔═══██╗████╗  ██║",
    r" ██║  ██║██████╔╝███████║█████╗  ██║  ██║██║   ██║██╔██╗ ██║",
    r" ██║  ██║██╔══██╗██╔══██║██╔══╝  ██║  ██║██║   ██║██║╚██╗██║",
    r" ██████╔╝██║  ██║██║  ██║███████╗██████╔╝╚██████╔╝██║ ╚████║",
    r" ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═══╝",
]


def _banner() -> None:
    console.print()
    for i, line in enumerate(BANNER):
        color = V if i < 3 else A
        console.print(f"[{color}]{line}[/{color}]")
        time.sleep(0.06)
    console.print(f"\n  [{DM}]passive recon framework  ·  v1.05[/{DM}]\n")
    time.sleep(0.15)


def _banner_static() -> None:
    console.print()
    for i, line in enumerate(BANNER):
        color = V if i < 3 else A
        console.print(f"[{color}]{line}[/{color}]")
    console.print(f"\n  [{DM}]passive recon framework  ·  v1.05[/{DM}]\n")


def _sep(width: int = 40) -> None:
    console.print(f"  [{DM}]{'─' * width}[/{DM}]")


def identify_target(s: str) -> str:
    s = s.strip()
    if re.match(r'^CVE-\d{4}-\d{4,}$', s, re.IGNORECASE):
        return "cve"
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', s):
        return "ip"
    if re.match(r'^https?://', s, re.IGNORECASE):
        return "url"
    if re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', s):
        return "email"
    if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9\-]+)+$', s):
        return "domain"
    return "unknown"


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
        padding=(0, 1),
        min_width=44,
    )
    table.add_column("Property", style=KY, no_wrap=True, min_width=16)
    table.add_column("Value", style=VL)

    for key, val in res.result_data.items():
        if val is None:
            continue
        display = ", ".join(str(v) for v in val) if isinstance(val, list) else str(val)
        table.add_row(key, display)

    console.print()
    console.print(table)
    console.print()


def _print_summary(results: list) -> None:
    _sep(38)
    ok_n   = sum(1 for r in results if r.success)
    fail_n = len(results) - ok_n
    summary = Text()
    summary.append("  scan complete  ·  ", style=DM)
    summary.append(f"{ok_n} ok", style=OK)
    summary.append("  ·  ", style=DM)
    summary.append(f"{fail_n} failed", style=ER if fail_n else DM)
    console.print(summary)
    console.print()


def _execute_modules(engine: Engine, modules_to_run: list, target: str) -> list:
    results = []
    for module in modules_to_run:
        with Live(
            Spinner("dots2", text=Text(f"  running  {module.name}...", style=DM)),
            console=console,
            refresh_per_second=20,
        ):
            result = module.run(target)
            engine.storage.save(result)
            results.append(result)
        _print_result(result)
    return results


def _run_autopilot(engine: Engine) -> bool:
    console.print()
    target = console.input(f"  [{A}]──› enter target : [/{A}]").strip()
    if not target:
        return False

    target_type = identify_target(target)
    if target_type == "unknown":
        console.print(f"\n  [{ER}]could not detect target type - please check your input[/{ER}]\n")
        return False

    info = Text()
    info.append("\n  target    ", style=DM)
    info.append(target, style=A)
    info.append("  ·  detected: ", style=DM)
    info.append(target_type, style=A)
    console.print(info)

    eligible = [m for m in engine.modules.values() if m.can_handle(target_type)]
    if not eligible:
        console.print(f"\n  [{ER}]no modules available for type: {target_type}[/{ER}]\n")
        return False

    console.print(f"  [{DM}]{len(eligible)} module(s) queued[/{DM}]\n")

    results = _execute_modules(engine, eligible, target)
    _print_summary(results)
    return True


def _run_manual(engine: Engine) -> bool:
    console.print()
    choices = [
        (f"{name}  [{', '.join(mod.supported_types)}]  -  {mod.description}", name)
        for name, mod in engine.modules.items()
    ]

    answers = inquirer.prompt([
        inquirer.Checkbox(
            "modules",
            message="Select modules to run  (Space to select, Enter to confirm)",
            choices=choices,
        ),
    ])
    if not answers or not answers["modules"]:
        console.print(f"\n  [{DM}]no modules selected[/{DM}]\n")
        return False

    selected_names   = answers["modules"]
    selected_modules = [engine.modules[n] for n in selected_names if n in engine.modules]

    console.print()
    target = console.input(f"  [{A}]--› enter target : [/{A}]").strip()
    if not target:
        return False

    info = Text()
    info.append("\n  target    ", style=DM)
    info.append(target, style=A)
    info.append(f"  ·  {len(selected_modules)} module(s) queued", style=DM)
    console.print(info)
    console.print()

    results = _execute_modules(engine, selected_modules, target)
    _print_summary(results)
    return True


def main() -> None:
    console.clear()
    _banner()

    buf = io.StringIO()
    with Live(
        Spinner("dots", text=Text("  initializing modules...", style=DM)),
        console=console,
        refresh_per_second=20,
    ):
        with contextlib.redirect_stdout(buf):
            engine = Engine()
        time.sleep(0.5)

    loaded = list(engine.modules.values())
    module_ready_line = f"  [{OK}]+  {len(loaded)} module(s) ready[/{OK}]\n"
    console.print(module_ready_line)

    first_iter = True
    while True:
        if not first_iter:
            console.clear()
            _banner_static()
            console.print(module_ready_line)
        first_iter = False

        answers = inquirer.prompt([
            inquirer.List(
                "mode",
                message="Select execution mode",
                choices=[
                    ("Auto-Pilot        detect type, run all matching modules", "auto"),
                    ("Manual Override   pick modules, then enter target",       "manual"),
                    ("Exit", "exit"),
                ],
            ),
        ])
        if not answers or answers["mode"] == "exit":
            console.print(f"\n  [{DM}]shutting down...[/{DM}]\n")
            return

        if answers["mode"] == "auto":
            ran = _run_autopilot(engine)
        else:
            ran = _run_manual(engine)

        if ran:
            console.print(f"  [bold {OK}]✔[/bold {OK}]  [{DM}]results have been logged to the database[/{DM}]")

        console.input(f"\n  [{DM}]press Enter to return to the main menu...[/{DM}]")


if __name__ == "__main__":
    main()
