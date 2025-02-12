from django.utils.deprecation import MiddlewareMixin

class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware pour ajouter des en-têtes HTTP de sécurité.
    """

    def process_response(self, request, response):
        response["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["Content-Security-Policy"] = "default-src 'self'"
        return response
