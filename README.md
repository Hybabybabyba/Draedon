<div align="center">

```
                                                                                                                                         
8 888888888o.      8 888888888o.            .8.          8 8888888888   8 888888888o.          ,o888888o.     b.             8           
8 8888    `^888.   8 8888    `88.          .888.         8 8888         8 8888    `^888.    . 8888     `88.   888o.          8           
8 8888        `88. 8 8888     `88         :88888.        8 8888         8 8888        `88. ,8 8888       `8b  Y88888o.       8           
8 8888         `88 8 8888     ,88        . `88888.       8 8888         8 8888         `88 88 8888        `8b .`Y888888o.    8           
8 8888          88 8 8888.   ,88'       .8. `88888.      8 888888888888 8 8888          88 88 8888         88 8o. `Y888888o. 8           
8 8888          88 8 888888888P'       .8`8. `88888.     8 8888         8 8888          88 88 8888         88 8`Y8o. `Y88888o8           
8 8888         ,88 8 8888`8b          .8' `8. `88888.    8 8888         8 8888         ,88 88 8888        ,8P 8   `Y8o. `Y8888           
8 8888        ,88' 8 8888 `8b.       .8'   `8. `88888.   8 8888         8 8888        ,88' `8 8888       ,8P  8      `Y8o. `Y8           
8 8888    ,o88P'   8 8888   `8b.    .888888888. `88888.  8 8888         8 8888    ,o88P'    ` 8888     ,88'   8         `Y8o.`           
8 888888888P'      8 8888     `88. .8'       `8. `88888. 8 888888888888 8 888888888P'          `8888888P'     8            `Yo 

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
git clone https://github.com/Hybabybabyba/draedon.git
cd draedon
pip install python-whois dnspython
```

---