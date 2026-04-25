<div align="center">

```
  ;                                               ;                                           
  ED.                                             ED.              :                          
  E#Wi                                          ,;E#Wi            t#,     L.                  
  E###G.       j.                             f#i E###G.         ;##W.    EW:        ,ft      
  E#fD#W;      EW,                   ..     .E#t  E#fD#W;       :#L:WE    E##;       t#E      
  E#t t##L     E##j                 ;W,    i#W,   E#t t##L     .KG  ,#D   E###t      t#E      
  E#t  .E#K,   E###D.              j##,   L#D.    E#t  .E#K,   EE    ;#f  E#fE#f     t#E      
  E#t    j##f  E#jG#W;            G###, :K#Wfff;  E#t    j##f f#.     t#i E#t D#G    t#E      
  E#t    :E#K: E#t t##f         :E####, i##WLLLLt E#t    :E#K::#G     GK  E#t  f#E.  t#E      
  E#t   t##L   E#t  :K#E:      ;W#DG##,  .E#L     E#t   t##L   ;#L   LW.  E#t   t#K: t#E      
  E#t .D#W;    E#KDDDD###i    j###DW##,    f#E:   E#t .D#W;     t#f f#:   E#t    ;#W,t#E      
  E#tiW#G.     E#f,t#Wi,,,   G##i,,G##,     ,WW;  E#tiW#G.       f#D#;    E#t     :K#D#E      
  E#K##i       E#t  ;#W:   :K#K:   L##,      .D#; E#K##i          G#t     E#t      .E##E      
  E##D.        DWi   ,KK: ;##D.    L##,        tt E##D.            t      ..         G#E      
  E#t                     ,,,      .,,            E#t                                 fE      
  L:                                              L:                                   ,      

```

**Modular Reconnaissance Framework**

[![Version](https://img.shields.io/badge/Version-1.1.0-8b5cf6?style=flat-square)](https://github.com/Hybabybabyba/draedon/releases)
[![Python](https://img.shields.io/badge/Python-3.10%2B-8b5cf6?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-6d28d9?style=flat-square)](LICENSE)
[![Modules](https://img.shields.io/badge/Modules-5-7c3aed?style=flat-square)](modules/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-4c1d95?style=flat-square)]()

</div>

---

**Draedon** is a modular, cross-platform reconnaissance framework built for passive and informational intelligence gathering. Designed around a clean plugin architecture - drop a file into `modules/`, and it works.

---

## Release - v1.1.0

**Draedon 1.1.0** is now available. This release significantly expands the module library and stabilizes the core engine.

**What's new:**
- `cert_search` - subdomain discovery via certificate transparency logs (crt.sh)
- `dns_brute` - passive subdomain brute-force via DNS resolution
- `tech_analyzer` - web stack detection from HTTP headers and page content
- Improved CLI menu and startup experience
- `draedon` alias now available after setup
- Bug fixes in engine module loading and storage layer

---

## Modules

| Module | Description | Target |
|--------|-------------|--------|
| `geoip` | IP geolocation via ip-api.com | `ip` |
| `whois` | Domain registration and ownership info | `domain` |
| `cert_search` | Subdomain discovery via crt.sh transparency logs | `domain` |
| `dns_brute` | Brute-force common subdomains via DNS resolution | `domain` |
| `tech_analyzer` | Detect web stack from HTTP headers and page content | `domain`, `url` |

---

## Installation

### Quick Start (all platforms)

**1. Clone the repository**

```bash
git clone https://github.com/Hybabybabyba/Draedon.git
cd Draedon
```

**2. Create and activate a virtual environment**

```bash
# Linux/macSos
python3 -m venv venv
source venv/bin/activate

# Windows (Powershell)
python -m venv venv
.\venv\Scripts\activate
```

**3. Upgrade build tools** *(crucial - skipping this causes install failures)*

```bash
pip install --upgrade pip setuptools wheel
```

**4. Install dependencies**

```bash
pip install -r requirements.txt
```

**5. Run**

```bash
python3 main.py        # Linux/macSos
python main.py         # Windows
```

---

## Global Access (optional)

Run `draedon` from any directory without activating the venv each time.

**Linux / macOS — shell alias**

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias draedon="source /path/to/Draedon/venv/bin/activate && python3 /path/to/Draedon/main.py"
```

Then reload: `source ~/.bashrc`

**Linux / macOS — launcher script**

```bash
sudo tee /usr/local/bin/draedon > /dev/null << 'EOF'
#!/usr/bin/env bash
source /path/to/Draedon/venv/bin/activate
python3 /path/to/Draedon/main.py "$@"
EOF
sudo chmod +x /usr/local/bin/draedon
```

**Windows — PowerShell alias**

Add to your `$PROFILE`:

```powershell
function draedon {
    & "C:\path\to\Draedon\venv\Scripts\python.exe" "C:\path\to\Draedon\main.py" @args
}
```

Replace `/path/to/Draedon` with the actual path where you cloned the repo.

---

## Usage

```bash
draedon
```

Results are saved automatically to `output/recon.db` (SQLite) after each run.


## Adding a Module

1. Create `modules/py_<name>.py`
2. Subclass `base_module`, set `self.name`, `self.description`, `self.supported_types`
3. Implement `run(self, target) -> module_result` - return `self.ok(data_dict)` or `self.fail(error_str)`
4. The engine picks it up automatically on next run — no registration needed

---

<div align="center">

MIT License · Built by [HybaBybaByba](https://github.com/HybaBybaByba)

</div>
