from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class SecurityMiddleware(MiddlewareMixin):
    """
    Middleware de sécurité pour protéger l'application contre certaines attaques.
    """

    # Liste noire d'IP bloquées
    BLOCKED_IPS = ["192.168.1.10", "45.33.32.156"]  # À modifier selon tes besoins

    # Liste des User-Agent interdits
    BLOCKED_USER_AGENTS = ["MaliciousBot", "BadCrawler"]

    def process_request(self, request):
        """ Vérification de la sécurité dès la réception de la requête """

        # 1️⃣ Vérifier si l'IP du client est bloquée
        ip = self.get_client_ip(request)
        if ip in self.BLOCKED_IPS:
            return JsonResponse({"error": "Accès interdit"}, status=403)

        # 2️⃣ Vérifier si le User-Agent est suspect
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        if not user_agent or any(bot in user_agent for bot in self.BLOCKED_USER_AGENTS):
            return JsonResponse({"error": "User-Agent interdit"}, status=403)

        # 3️⃣ Protection CSRF (si pas déjà géré par Django)
        if request.method in ["POST", "PUT", "DELETE"]:
            csrf_token = request.META.get("HTTP_X_CSRF_TOKEN")
            if not csrf_token:
                return JsonResponse({"error": "CSRF Token manquant"}, status=403)

    def process_response(self, request, response):
        """ Ajout d'en-têtes de sécurité aux réponses HTTP """

        # 4️⃣ Ajout des headers HTTP de sécurité
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["Referrer-Policy"] = "no-referrer"
        response["X-XSS-Protection"] = "1; mode=block"

        return response

    def get_client_ip(self, request):
        """ Récupère l'IP du client en prenant en compte les proxys """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
