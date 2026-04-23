import os
import shodan
from core.base_module import base_module, module_result


class shodan_module(base_module):
    name        = "shodan"
    description = "Shodan scan: ports, vulns, org, OS"
    accepts     = ["shodan"]
    
    def run(self, target: str) -> module_result:
        api_key = os.getenv("SHODAN_API_KEY")
        if not api_key:
            return self.fail(target, "SHODAN_API_KEY is not set")

        try:
            api  = shodan.Shodan(api_key)
            host = api.host(target)

            ports = sorted({item["port"] for item in host.get("data", [])})
            vulns = list(host.get("vulns", {}).keys())

            return self.ok(target, {
                "ip":     host.get("ip_str"),
                "org":    host.get("org"),
                "isp":    host.get("isp"),
                "os":     host.get("os"),
                "ports":  ports,
                "vulns":  vulns if vulns else None,
            })

        except shodan.APIError as e:
            return self.fail(target, f"Shodan API error: {e}")
        except Exception as e:
            return self.fail(target, str(e))
