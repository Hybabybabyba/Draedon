import requests
from core.base_module import base_module, module_result

class cert_search_module(base_module):
    name = "cert_search"
    description = "Find subdomains via certificate transparency logs (crt.sh)"
    supported_types = ["domain"]

    def run(self, target: str) -> module_result:
        url = f"https://crt.sh/?q=%.{target}&output=json"
        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            resp.raise_for_status()
            entries = resp.json()
        except requests.exceptions.Timeout:
            return self.fail(target, "crt.sh request timed out")
        except requests.exceptions.ConnectionError:
            return self.fail(target, "Could not connect to crt.sh")
        except Exception as e:
            return self.fail(target, str(e))

        subdomains = set()
        for entry in entries:
            name_value = entry.get("name_value", "")
            for name in name_value.splitlines():
                name = name.strip().lstrip("*.")
                if name and target in name:
                    subdomains.add(name)

        if not subdomains:
            return self.fail(target, "No certificate records found")

        sorted_subs = sorted(subdomains)
        return self.ok(target, {"count": len(sorted_subs), "subdomains": sorted_subs})
