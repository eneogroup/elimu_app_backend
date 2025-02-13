from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from api.serializers.school_manager_serializer import UserRegistrationSerializer
from backend.constant import get_user_school
from backend.models.account import User
from api.serializers.account_serializer import PasswordResetConfirmSerializer, PasswordResetSerializer,  UserRoleSerializer, UserSerializer
from rest_framework import status, views

from backend.models.school_manager import Classroom, SchoolYear, UserRegistration
from backend.permissions.permission_app import IsManager, IsDirector

User = get_user_model()

class UserRoleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated] 

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager,IsDirector]



class CurrentUserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Retourne les informations de l'utilisateur connecté.
        """
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class PasswordResetView(views.APIView):
    """
    API pour réinitialiser le mot de passe via email.
    """
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request)
            return Response({"detail": "Un email de réinitialisation de mot de passe a été envoyé."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(views.APIView):
    """
    Vue API pour confirmer le nouveau mot de passe après la réinitialisation.
    """
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Mot de passe changé avec succès."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PupilsViewSet(viewsets.ViewSet):
    """
    ViewSet pour gérer la liste et les détails des élèves d'une école.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request):
        """
        Récupérer la liste des élèves de l'école de l'utilisateur connecté.
        """
        school = request.session.get('school')  # Récupérer l'école en session
        pupils = UserRegistration.objects.filter(
            school=school,
            user__roles__name__iexact="Élève"
        )
        serializer = UserSerializer(pupils, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Récupérer les détails d'un élève spécifique.
        """
        school = request.session.get('school')
        pupil = get_object_or_404(
            UserRegistration, school=school, user__id=pk, user__roles__name__iexact="Élève"
        )
        serializer = UserSerializer(pupil)
        return Response(serializer.data)



class ParentsViewSet(viewsets.ViewSet):
    """
    ViewSet pour gérer la liste et les détails des parents d'une école.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    
    def list(self, request):
        """
        Récupérer la liste des parents de l'école de l'utilisateur connecté.
        """
        school = request.session.get('school')  # Récupérer l'école en session
        parents = UserRegistration.objects.filter(
            school=school,
            user__roles__name__iexact="Parent"
        )
        serializer = UserSerializer(parents, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Récupérer les détails d'un parent spécifique.
        """
        school = request.session.get('school')
        parent = get_object_or_404(
            UserRegistration, school=school, user__id=pk, user__roles__name__iexact="Parent"
        )
        serializer = UserSerializer(parent)
        return Response(serializer.data)


class TeachersViewSet(viewsets.ViewSet):
    """
    ViewSet pour gérer la liste et les détails des enseignants d'une école.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """
        Récupérer la liste des enseignants de l'école de l'utilisateur connecté.
        """
        school = request.session.get('school')  # Récupérer l'école en session
        teachers = UserRegistration.objects.filter(
            school=school,
            user__roles__name__iexact="Enseignant"
        )
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Récupérer les détails d'un enseignant spécifique.
        """
        school = request.session.get('school')
        teacher = get_object_or_404(
            UserRegistration, school=school, user__id=pk, user__roles__name__iexact="Enseignant"
        )
        serializer = UserSerializer(teacher)
        return Response(serializer.data)


class RegistrationPupilByMatricule(views.APIView):
    """
    Vue API pour créer un élève à partir de son matricule.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, matricule=None, classroom_id=None):
        """
        Créer un élève à partir de son matricule et l'affecter à une classe.
        """
        school = request.session.get('school')
        
        if not school:
            return Response({"detail": "Aucune école associée à la session."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupération de l'utilisateur ou renvoi d'une erreur 404
        user = get_object_or_404(User, matricule=matricule)

        # Vérifier que l'utilisateur est bien un élève
        if not user.roles.filter(name__iexact="Élève").exists():
            return Response({"detail": "L'utilisateur n'est pas un élève."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupération de la classe
        classroom = get_object_or_404(Classroom, id=classroom_id)

        # Récupération de l'année scolaire actuelle
        academic_year = SchoolYear.objects.filter(school=school, is_current_year=True).first()
        if not academic_year:
            return Response({"detail": "Aucune année scolaire active trouvée."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si l'élève est déjà inscrit
        if UserRegistration.objects.filter(school=school, user=user, school_year=academic_year).exists():
            return Response({"detail": "Élève déjà inscrit pour cette année scolaire."}, status=status.HTTP_400_BAD_REQUEST)

        # Création et enregistrement de l'inscription
        pupil_registered = UserRegistration(school=school, user=user, classroom=classroom, school_year=academic_year)
        pupil_registered.save()

        # Sérialisation et retour de la réponse
        serializer = UserRegistrationSerializer(pupil_registered)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationParentByMatricul(views.APIView):
    """
    Vue API pour créer un parent à partir de son matricule.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, matricule=None, classroom_id=None):
        """
        Créer un parent à partir de son matricule et l'affecter à une classe.
        """
        school = request.session.get('school')
        
        if not school:
            return Response({"detail": "Aucune école associée à la session."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupération de l'utilisateur ou renvoi d'une erreur 404
        user = get_object_or_404(User, matricule=matricule)

        # Vérifier que l'utilisateur est bien un parent
        if not user.roles.filter(name__iexact="Parent").exists():
            return Response({"detail": "L'utilisateur n'est pas un parent."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupération de l'année scolaire actuelle
        academic_year = SchoolYear.objects.filter(school=school, is_current_year=True).first()
        if not academic_year:
            return Response({"detail": "Aucune année scolaire active trouvée."}, status=status.HTTP_400_BAD_REQUEST)

        # Vérifier si le parent est déjà inscrit
        if UserRegistration.objects.filter(school=school, user=user, school_year=academic_year).exists():
            return Response({"detail": "Le parent est déjà inscrit pour cette année scolaire."}, status=status.HTTP_400_BAD_REQUEST)

        # Création et enregistrement de l'inscription
        parent_registered = UserRegistration(school=school, user=user, school_year=academic_year)
        parent_registered.save()

        # Sérialisation et retour de la réponse
        serializer = UserRegistrationSerializer(parent_registered)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegistrationTeacherByMatricul(views.APIView):
    """
    Vue API pour créer un enseigant à partir de son matricule.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, matricule=None):
        """
        Créer un enseigant à partir de son matricule et l'affecter à une classe.
        """
        school = request.session.get('school')
        
        if not school:
            return Response({"detail": "Aucune école associée à la session."}, status=status.HTTP_400_BAD_REQUEST)

        # Récupération de l'utilisateur ou renvoi d'une erreur 404
        user = get_object_or_404(User, matricule=matricule)

        # Vérifier que l'utilisateur est bien un élève
        if not user.roles.filter(name__iexact="Enseignant").exists():
            return Response({"detail": "L'utilisateur n'est pas un enseignant."}, status=status.HTTP_400_BAD_REQUEST)


        # Vérifier si l'enseigant est déjà inscrit
        if UserRegistration.objects.filter(school=school, user=user).exists():
            return Response({"detail": "L'enseignant est déjà inscrit dans cette école."}, status=status.HTTP_400_BAD_REQUEST)

        # Création et enregistrement de l'inscription
        teacher_registered = UserRegistration(school=school, user=user)
        teacher_registered.save()

        # Sérialisation et retour de la réponse
        serializer = UserRegistrationSerializer(teacher_registered)
        return Response(serializer.data, status=status.HTTP_201_CREATED)




"""
   #Rest des vues à ajourter pour ce fichier
        [
            Vue API pour créer un élève à partir de ses informations.
            Vue API pour créer un parent à partir de ses informations.
            Vue API pour créer un enseignant à partir de ses informations.
            Vue API pour créer un utilisateur de rôle spécifique(gestionnaire, comptable, etc...)
            Vue API pour modifier les informations d'un utilisateur.
        ]
"""