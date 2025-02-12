from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.contrib.auth.middleware import get_user

class RoleRestrictionMiddleware(MiddlewareMixin):
    """
    Middleware pour restreindre l'accès à certaines vues en fonction du rôle de l'utilisateur.
    """

    # Définition des routes protégées et des rôles autorisés
    ROLE_RESTRICTIONS = {
        "admin-only": ["ADMIN"],  # Routes accessibles uniquement aux administrateurs
        "teacher-only": ["ADMIN", "TEACHER"],  # Routes accessibles aux admins et enseignants
        "student-only": ["STUDENT"],  # Routes accessibles uniquement aux étudiants
    }

    PROTECTED_URLS = {
        "/api/admin-dashboard/": "admin-only",
        "/api/manage-classes/": "teacher-only",
        "/api/student-homework/": "student-only",
    }

    def process_request(self, request):
        """ Vérification des autorisations avant l'accès aux vues. """
        
        # Récupérer l'URL actuelle
        path = request.path_info
        
        # Vérifier si l'URL est protégée
        for protected_path, role_key in self.PROTECTED_URLS.items():
            if path.startswith(protected_path):
                
                # Récupérer l'utilisateur connecté
                user = get_user(request)
                
                if not user.is_authenticated:
                    return JsonResponse({"error": "Authentification requise"}, status=401)

                # Récupérer le rôle de l'utilisateur
                user_role = getattr(user, "roles", None)  # Assure-toi que le modèle User a un champ `role`
                
                # Vérifier si l'utilisateur a l'autorisation d'accès
                allowed_roles = self.ROLE_RESTRICTIONS.get(role_key, [])
                if user_role not in allowed_roles:
                    return JsonResponse({"error": "Accès interdit"}, status=403)

        return None  # Continuer normalement si tout est bon


from django.http import JsonResponse
from django.urls import resolve
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

# Définition des routes protégées et des rôles requis
PROTECTED_ROUTES = {
    'school-years': ['admin', 'school_manager'],
    'active-schoolyear': ['admin', 'school_manager'],
    'classrooms': ['admin', 'school_manager'],
    'inscriptions': ['admin', 'school_manager'],
    'student-evaluations': ['admin', 'teacher'],
    'school-statistics': ['admin', 'school_manager'],
    'students': ['admin', 'school_manager'],
    'pupils': ['admin', 'school_manager'],
    'subject-attributions': ['admin', 'school_manager'],
    'school-report-cards': ['admin', 'teacher'],
    'school-invoices': ['admin', 'accountant'],
    'ebooks': ['admin', 'library_manager'],
    'announcements': ['admin', 'communication_manager'],
}

class RoleBasedAccessMiddleware:
    """
    Middleware pour restreindre l'accès aux vues selon le rôle de l'utilisateur et vérifier la session.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Récupération de la vue associée à l'URL
        resolver_match = resolve(request.path)
        view_name = resolver_match.url_name

        # Vérifie si la route est protégée
        for route, allowed_roles in PROTECTED_ROUTES.items():
            if route in request.path:
                # Vérifie si l'utilisateur est authentifié
                try:
                    user, _ = JWTAuthentication().authenticate(request)
                    if not user:
                        raise AuthenticationFailed("Authentification requise")
                except AuthenticationFailed:
                    return JsonResponse({'error': "Authentification requise"}, status=401)

                # Vérifie si le school_code est en session
                if "school_code" not in request.session:
                    return JsonResponse({'error': "Code d'établissement requis"}, status=403)

                # Vérifie si le rôle de l'utilisateur est autorisé
                if user.role not in allowed_roles:
                    return JsonResponse({'error': "Accès interdit"}, status=403)

        return self.get_response(request)
