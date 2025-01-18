from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import authenticate, login, logout
from backend.models.account import User
from backend.models.school_manager import School



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }



class LoginViewSet(viewsets.ViewSet):
    """
    ViewSet pour gérer le login des utilisateurs.
    """

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        # Récupération des données du corps de la requête
        username = request.data.get('username')
        password = request.data.get('password')
        code = request.data.get('school_code')

        # Vérification de l'existence de l'école
        try:
            school = School.objects.filter(code=code).first()
        except School.DoesNotExist:
            return Response({"errors": "Aucun établissement ne correspond à ce code"}, status=status.HTTP_404_NOT_FOUND)

        # Vérification de l'existence de l'utilisateur lié à l'école
        try:
            user = User.objects.filter(school_code=school, username=username).first()
            if not user:
                raise User.DoesNotExist
        except User.DoesNotExist:
            return Response({"errors": "Aucun utilisateur ne correspond à cet établissement"}, status=status.HTTP_404_NOT_FOUND)

        # Authentification de l'utilisateur
        user = authenticate(username=username, password=password)
        if user is not None:
            # Connexion de l'utilisateur
            login(request, user)
            token = get_tokens_for_user(user)  # Fonction pour générer le token (JWT ou autre)
            return Response(token, status=status.HTTP_200_OK)

        # Retour en cas d'échec de l'authentification
        return Response({"errors": "Nom d'utilisateur ou mot de passe incorrect !"}, status=status.HTTP_400_BAD_REQUEST)



class LogoutAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Obtenir le token d'accès depuis le header Authorization
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header:
                token = auth_header.split()[1]  # 'Bearer <token>'

                # Récupérer l'instance OutstandingToken
                outstanding_token = OutstandingToken.objects.get(token=token)

                # Blacklister le token
                BlacklistedToken.objects.create(token=outstanding_token)
                
                return Response({'message': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)
            else:
                return Response({'error': 'Token not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        except OutstandingToken.DoesNotExist:
            return Response({'error': 'Token does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)