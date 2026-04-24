import requests
from core.base_module import base_module, module_result

CMS_PATTERNS = {
    "WordPress":  ["wp-content", "wp-includes", "wp-json"],
    "Joomla":     ["option=com_", "/components/com_"],
    "Drupal":     ["sites/default/files", "Drupal.settings"],
    "Magento":    ["Mage.Cookies", "/skin/frontend/"],
    "Shopify":    ["cdn.shopify.com", "myshopify.com"],
    "Laravel":    ["laravel_session", "XSRF-TOKEN"],
    "Django":     ["csrfmiddlewaretoken", "django"],
    "Next.js":    ["__NEXT_DATA__", "_next/static"],
    "React":      ["__react", "data-reactroot"],
}

class tech_analyzer_module(base_module):
    name = "tech_analyzer"
    description = "Detect web stack from HTTP headers and page content"
    supported_types = ["domain", "url"]

    def run(self, target: str) -> module_result:
        url = target if target.startswith(("http://", "https://")) else f"https://{target}"
        tech = {}

        try:
            resp = requests.get(url, timeout=8, allow_redirects=True,
                                headers={"User-Agent": "Mozilla/5.0"})
        except requests.exceptions.SSLError:
            try:
                resp = requests.get(url.replace("https://", "http://"), timeout=8,
                                    allow_redirects=True,
                                    headers={"User-Agent": "Mozilla/5.0"})
            except Exception as e:
                return self.fail(target, str(e))
        except Exception as e:
            return self.fail(target, str(e))

        headers = {k.lower(): v for k, v in resp.headers.items()}
        body = resp.text

        if "server" in headers:
            tech["server"] = headers["server"]
        if "x-powered-by" in headers:
            tech["x-powered-by"] = headers["x-powered-by"]
        if "x-generator" in headers:
            tech["x-generator"] = headers["x-generator"]
        if "x-framework" in headers:
            tech["x-framework"] = headers["x-framework"]

        cookie_header = headers.get("set-cookie", "")
        if "PHPSESSID" in cookie_header:
            tech.setdefault("language", "PHP")
        if "ASP.NET_SessionId" in cookie_header or "ASPSESSIONID" in cookie_header:
            tech.setdefault("language", "ASP.NET")

        detected_cms = []
        for cms, patterns in CMS_PATTERNS.items():
            if any(p in body for p in patterns):
                detected_cms.append(cms)
        if detected_cms:
            tech["cms"] = detected_cms

        tech["status_code"] = resp.status_code
        tech["final_url"] = resp.url

        return self.ok(target, tech)
