import socket
from core.base_module import base_module, module_result

COMMON_SUBDOMAINS = [
    "www", "mail", "admin", "dev", "test", "vpn", "api",
    "stage", "staging", "ftp", "ssh", "mx", "ns1", "ns2",
    "blog", "shop", "portal", "remote", "cdn", "static",
]

class dns_brute_module(base_module):
    name = "dns_brute"
    description = "Brute-force common subdomains via DNS resolution"
    supported_types = ["domain"]

    def run(self, target: str) -> module_result:
        found = {}
        for sub in COMMON_SUBDOMAINS:
            hostname = f"{sub}.{target}"
            try:
                ip = socket.gethostbyname(hostname)
                found[hostname] = ip
            except socket.gaierror:
                pass
            except Exception:
                pass

        if not found:
            return self.fail(target, "No subdomains resolved")

        return self.ok(target, {"count": len(found), "subdomains": found})
