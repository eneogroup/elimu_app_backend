import time
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class BruteForceProtectionMiddleware(MiddlewareMixin):
    """
    Middleware pour protéger contre les attaques Brute-Force sur la connexion.
    """

    MAX_ATTEMPTS = 5  # Nombre maximal de tentatives avant blocage
    BLOCK_TIME = 300  # Temps de blocage en secondes (5 minutes)

    def process_request(self, request):
        """ Vérifie si l'IP ou l'utilisateur est bloqué avant d'autoriser la requête """
        
        # On cible uniquement l'endpoint de connexion
        if request.path.startswith("/api/auth/login/") and request.method == "POST":
            ip = self.get_client_ip(request)
            username = request.POST.get("username", "")

            # Vérifier si l'IP est bloquée
            if cache.get(f"blocked_ip:{ip}"):
                return JsonResponse({"error": "Trop de tentatives. Réessayez plus tard."}, status=429)

            # Vérifier si l'utilisateur est bloqué
            if cache.get(f"blocked_user:{username}"):
                return JsonResponse({"error": "Trop de tentatives. Réessayez plus tard."}, status=429)

    def process_response(self, request, response):
        """ Gère l'enregistrement des tentatives de connexion échouées """

        if request.path.startswith("/api/auth/login/") and request.method == "POST":
            ip = self.get_client_ip(request)
            username = request.POST.get("username", "")

            # Si la connexion échoue, on enregistre l'échec
            if response.status_code in [400, 401]:
                self.increment_attempts(ip, username)

        return response

    def get_client_ip(self, request):
        """ Récupère l'adresse IP du client """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def increment_attempts(self, ip, username):
        """ Incrémente les tentatives de connexion et bloque en cas d'abus """

        ip_attempts = cache.get(f"attempts_ip:{ip}", 0)
        user_attempts = cache.get(f"attempts_user:{username}", 0)

        ip_attempts += 1
        user_attempts += 1

        # Met à jour le cache avec un TTL de 5 minutes
        cache.set(f"attempts_ip:{ip}", ip_attempts, timeout=self.BLOCK_TIME)
        cache.set(f"attempts_user:{username}", user_attempts, timeout=self.BLOCK_TIME)

        if ip_attempts >= self.MAX_ATTEMPTS:
            cache.set(f"blocked_ip:{ip}", True, timeout=self.BLOCK_TIME)

        if user_attempts >= self.MAX_ATTEMPTS:
            cache.set(f"blocked_user:{username}", True, timeout=self.BLOCK_TIME)
