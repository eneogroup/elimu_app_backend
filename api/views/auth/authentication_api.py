# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate, login, logout

# from backend.models.gestion_ecole import Etablishment
# from backend.models.user_account import User

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)

#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     }


# class LoginAPIView(APIView):

#     def post(self, request, format=None):
#         username = request.data['username']
#         password = request.data['password']
#         code = request.data['code']
#         try:
#             school = Etablishment.objects.get(code=code)
#         except Etablishment.DoesNotExist:
#             return Response({"errors:":"Aucun établissement ne corresponds à ce code"}, status=status.HTTP_404_NOT_FOUND)
        
#         try:
#            User.objects.get(school=school, username=username)
#         except User.DoesNotExist:
#             return Response({"errors:":"ERREUR: Aucun utilisateur ne corresponds à cet établissement"}, status=status.HTTP_404_NOT_FOUND)
        
#         user = authenticate(username=username, password=password)
        
#         if user is not None:
#             login(request,user)
#             token = get_tokens_for_user(user)
#             return Response(token, status=status.HTTP_200_OK)
        
#         return Response({"errors:":"Username or password incorrect !"}, status=status.HTTP_400_BAD_REQUEST)

# class LogoutAPIView(APIView):

#     def get(self, request, format=None):
#         if request.user.is_authenticated:
#             logout(request)
#             return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
        
#         return Response({"error": "Aucun utilisateur connecté"}, status=status.HTTP_400_BAD_REQUEST)

