import time
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from backend.models import AccessLog  # Assurez-vous que le chemin est correct

# Configuration du logger
logger = logging.getLogger("access_logger")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler("access_logs.log")  # Enregistrement dans un fichier
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

class AccessLoggingMiddleware(MiddlewareMixin):
    """
    Middleware pour journaliser les requêtes entrantes et sortantes.
    """

    def process_request(self, request):
        """ Capture le début de la requête pour mesurer le temps de réponse """
        request.start_time = time.time()

    def process_response(self, request, response):
        """ Journalise les informations sur chaque requête traitée """

        # Calcul du temps de réponse
        duration = time.time() - getattr(request, "start_time", time.time())

        # Récupération de l'utilisateur
        user = request.user if hasattr(request, "user") and request.user.is_authenticated else None

        # Récupération de l'adresse IP
        ip = self.get_client_ip(request)

        # Sauvegarde en base de données
        AccessLog.objects.create(
            user=user,
            ip_address=ip,
            method=request.method,
            path=request.get_full_path(),
            status_code=response.status_code,
            response_time=round(duration, 3),
        )

        # Enregistrement dans le fichier log
        logger.info(f"User: {user}, IP: {ip}, {request.method} {request.get_full_path()} -> {response.status_code} ({round(duration, 3)}s)")

        return response

    def get_client_ip(self, request):
        """ Récupère l'adresse IP du client """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
