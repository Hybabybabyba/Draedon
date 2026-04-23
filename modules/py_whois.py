import whois
from core.base_module import base_module, module_result

class whois_module(base_module):
    name        = "whois"
    description = "Whois info about domain"
    accepts     = ["domain"]

    def run(self, target: str) -> module_result:
        try:
            w = whois.whois(target)
            def fmt_date(d):
                if isinstance(d, list):
                    d = d[0]
                return str(d) if d else None
                
            return self.ok(target, {
                "domain":      w.domain_name,
                "registrar":   w.registrar,
                "created":     fmt_date(w.creation_date),
                "expires":     fmt_date(w.expiration_date),
                "updated":     fmt_date(w.updated_date),
            })

        except Exception as e:
            return self.fail(target, str(e))