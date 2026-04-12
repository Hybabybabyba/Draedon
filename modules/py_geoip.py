import json
import urllib.request
from core.base_module import base_module, module_result


class geoIPmodule(base_module):
    name        = "geoip"
    description = "GEO of ip:"
    accepts     = ["ip"]

    def run(self, target: str) -> module_result:
        url = (
            f"http://ip-api.com/json/{target}"
            f"?fields=status,country,regionName,city,isp,org,lat,lon,timezone,query"
        )
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())

            if data.get("status") != "success":
                return self.fail(target, "IP not found GEO")

            return self.ok(target, {
                "ip":       data.get("query"),
                "country":  data.get("country"),
                "region":   data.get("regionName"),
                "city":     data.get("city"),
                "isp":      data.get("isp"),
                "org":      data.get("org"),
                "lat":      data.get("lat"),
                "lon":      data.get("lon"),
                "timezone": data.get("timezone"),
            })
        except Exception as e:
            return self.fail(target, str(e))