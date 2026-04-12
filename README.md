<div align="center">

```
oooooooooo.   ooooooooo.         .o.       oooooooooooo oooooooooo.     .oooooo.   ooooo      ooo      
`888'   `Y8b  `888   `Y88.      .888.      `888'     `8 `888'   `Y8b   d8P'  `Y8b  `888b.     `8'      
 888      888  888   .d88'     .8"888.      888          888      888 888      888  8 `88b.    8       
 888      888  888ooo88P'     .8' `888.     888oooo8     888      888 888      888  8   `88b.  8       
 888      888  888`88b.      .88ooo8888.    888    "     888      888 888      888  8     `88b.8       
 888     d88'  888  `88b.   .8'     `888.   888       o  888     d88' `88b    d88'  8       `888       
o888bood8P'   o888o  o888o o88o     o8888o o888ooooood8 o888bood8P'    `Y8bood8P'  o8o        `8       
                                                                                          
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
