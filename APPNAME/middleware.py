from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

class CustomCSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if hasattr(settings, "CSP") and "DIRECTIVES" in settings.CSP:
            policy_parts = []
            for directive, sources in settings.CSP["DIRECTIVES"].items():
                part = f"{directive} {' '.join(sources)}"
                policy_parts.append(part)
            response["Content-Security-Policy"] = "; ".join(policy_parts)
        return response
