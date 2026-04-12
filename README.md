<div align="center">

```
 ██████████   ███████████     █████████   ██████████ ██████████      ███████    ██████   █████
░░███░░░░███ ░░███░░░░░███   ███░░░░░███ ░░███░░░░░█░░███░░░░███   ███░░░░░███ ░░██████ ░░███ 
 ░███   ░░███ ░███    ░███  ░███    ░███  ░███  █ ░  ░███   ░░███ ███     ░░███ ░███░███ ░███ 
 ░███    ░███ ░██████████   ░███████████  ░██████    ░███    ░███░███      ░███ ░███░░███░███ 
 ░███    ░███ ░███░░░░░███  ░███░░░░░███  ░███░░█    ░███    ░███░███      ░███ ░███ ░░██████ 
 ░███    ███  ░███    ░███  ░███    ░███  ░███ ░   █ ░███    ███ ░░███     ███  ░███  ░░█████ 
 ██████████   █████   █████ █████   █████ ██████████ ██████████   ░░░███████░   █████  ░░█████
░░░░░░░░░░   ░░░░░   ░░░░░ ░░░░░   ░░░░░ ░░░░░░░░░░ ░░░░░░░░░░      ░░░░░░░    ░░░░░    ░░░░░ 
                                                                                              
                                                                                              
                                                                                              
```

**Modular Reconnaissance Framework**

[![Python](https://img.shields.io/badge/Python-3.10%2B-8b5cf6?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-6d28d9?style=flat-square)](LICENSE)
[![Modules](https://img.shields.io/badge/Modules-3-7c3aed?style=flat-square)](modules/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-4c1d95?style=flat-square)]()

</div>

---

**Draedon** is a modular, cross-platform reconnaissance framework built for passive and informational intelligence gathering. Designed around a clean plugin architecture — drop a file into `modules/`, and it works.

---

## Modules

| Name | Description | Target |
|------|-------------|--------|
| `geoip` | IP geolocation via ip-api.com | `ip` |
| `whois` | Domain registration info | `domain` |
| `dns` | DNS records — A, MX, TXT, NS, CNAME, SPF, DMARC | `domain` |

---

## Installation

```bash
git clone https://github.com/yourusername/draedon.git
cd draedon
pip install python-whois dnspython
```

---

## Usage

```bash
python main.py 8.8.8.8
python main.py google.com --type domain
python main.py --list
```

---

<div align="center">
<sub>Built with silence and purpose.</sub>
</div>
