from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.contrib.auth import authenticate, login, logout

from backend.models.account import User
from backend.models.school_manager import School

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginAPIView(APIView):

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        code = request.data['school_code']
        try:
            school = School.objects.filter(code=code).first()
        except School.DoesNotExist:
            return Response({"errors:":"Aucun établissement ne corresponds à ce code"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
           User.objects.filter(school_code=school, username=username).filter()
        except User.DoesNotExist:
            return Response({"errors:":"ERREUR: Aucun utilisateur ne corresponds à cet établissement"}, status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username=username, password=password)
        print(user)
        
        if user is not None:
            login(request,user)
            token = get_tokens_for_user(user)
            return Response(token, status=status.HTTP_200_OK)
        
        return Response({"errors:":"Username or password incorrect !"}, status=status.HTTP_400_BAD_REQUEST)


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