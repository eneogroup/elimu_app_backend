import logging
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from api.serializers.school_manager_serializer import SchoolSerializer
from backend.models.account import User
from backend.models.school_manager import School, SchoolYear, UserRegistration
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
logger = logging.getLogger(__name__)

def get_tokens_for_user(user, school):
    refresh = RefreshToken.for_user(user)
    refresh['school'] = SchoolSerializer(school).data
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
        username = request.data.get('username')
        password = request.data.get('password')
        code = request.data.get('school_code')

        # Vérifier l'existence de l'école
        school = School.objects.filter(code=code).first()
        if not school:
            return Response({"errors": "Aucun établissement ne correspond à ce code"}, status=status.HTTP_404_NOT_FOUND)

        # Vérifier l'existence de l'utilisateur lié à l'école
        user = User.objects.filter(username=username, school=school).first()

        if not user:
            current_academic_year = SchoolYear.objects.filter(is_current_year=True, school=school).first()
            user_request = User.objects.filter(username=username).first()
            user = UserRegistration.objects.filter(school=school, school_year=current_academic_year, user=user_request).first()

        if not user:
            return Response({"errors": "Aucun utilisateur ne correspond à cet établissement"}, status=status.HTTP_404_NOT_FOUND)

        # Authentifier l'utilisateur avec son mot de passe
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            # Connexion et génération du token
            login(request, user)
            token = get_tokens_for_user(user, school)
            return Response(token, status=status.HTTP_200_OK)

        return Response({"errors": "Nom d'utilisateur ou mot de passe incorrect !"}, status=status.HTTP_400_BAD_REQUEST)





class LogoutAPIView(generics.GenericAPIView):
    """
    Endpoint pour déconnecter un utilisateur en blacklistant son token d'accès.
    L'utilisateur doit être authentifié.
    """
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        return None

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except (TokenError, InvalidToken):
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

