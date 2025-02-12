from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import authenticate, login, logout
from backend.models.account import User
from backend.models.school_manager import School, SchoolYear, UserRegistration



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
        user = authenticate(request, username=user.user.username, password=password)

        if user is not None:
            # Connexion et génération du token
            login(request, user)
            token = get_tokens_for_user(user)
            request.session["school"] = school
            return Response(token, status=status.HTTP_200_OK)

        return Response({"errors": "Nom d'utilisateur ou mot de passe incorrect !"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(generics.GenericAPIView):
    """
    Endpoint pour déconnecter un utilisateur en blacklistant son token d'accès.
    L'utilisateur doit être authentifié.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Vérifier si le header Authorization est présent et valide
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if not auth_header.startswith('Bearer '):
                return Response(
                    {'error': 'Invalid or missing Authorization header.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Extraire le token depuis le header
            token = auth_header.split()[1]
            print(token)

            # Rechercher le token dans OutstandingToken
            try:
                outstanding_token = OutstandingToken.objects.get(token=token)
            except OutstandingToken.DoesNotExist:
                return Response(
                    {'error': 'Token does not exist or is already invalidated.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Blacklister le token
            BlacklistedToken.objects.create(token=outstanding_token)

            return Response(
                {'message': 'Logout successful.'},
                status=status.HTTP_205_RESET_CONTENT
            )

        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )