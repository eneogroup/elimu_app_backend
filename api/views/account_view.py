from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from backend.models.account import ParentOfStudent, Pupil, TeacherSchool, User
from api.serializers.account_serializer import ParentOfStudentSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer, PupilSerializer, TeacherSerializer, UserRoleSerializer, UserSerializer
from rest_framework import status, views

from backend.models.school_manager import Inscription
from backend.permissions.permission_app import IsManager, IsDirector

User = get_user_model()

class UserRoleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated] 

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager,IsDirector]

    def get_permissions(self):
        """
        Retourne les permissions en fonction de l'action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Seuls les gestionnaires ou directeurs peuvent créer, modifier ou supprimer des utilisateurs
            return [IsManager() or IsDirector()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Filtrer les utilisateurs pour permettre à chaque utilisateur de voir ses propres données
        ou, si c'est un gestionnaire ou directeur, de voir tout le monde dans son école.
        """
        user = self.request.user
        if user.role.filter(name__in=['Gestionnaire', 'Directeur']).exists():
            # Les gestionnaires et directeurs voient tous les utilisateurs de leur école
            return User.objects.filter(school_code=user.school_code)
        # Autres utilisateurs voient uniquement leur propre compte
        return User.objects.filter(id=user.id, school_code=user.school_code)

    def perform_create(self, serializer):
        """
        Associer l'utilisateur à l'école de l'utilisateur connecté lors de la création.
        """
        serializer.save(school_code=self.request.user.school_code)

    def create(self, request, *args, **kwargs):
        """
        Personnaliser la création pour inclure automatiquement le code de l'école.
        """
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Empêcher les utilisateurs de modifier les informations des utilisateurs d'une autre école.
        """
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response(
                {"detail": "Vous ne pouvez pas modifier cet utilisateur."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Empêcher les utilisateurs de supprimer un utilisateur d'une autre école.
        """
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response(
                {"detail": "Vous ne pouvez pas supprimer cet utilisateur."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


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

class TeacherSchoolViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TeacherSerializer

    def get_queryset(self):
        # Filtrer les enseignants par l'école de l'utilisateur connecté
        return TeacherSchool.objects.filter(school_code=self.request.user.school_code)

    def perform_create(self, serializer):
        # Associer l'enseignant à l'école de l'utilisateur connecté
        serializer.save(school_code=self.request.user.school_code)

    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # S'assurer que l'utilisateur ne modifie pas l'école d'un enseignant
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cet enseignant."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # S'assurer que l'utilisateur ne supprime pas un enseignant d'une autre école
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cet enseignant."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class ParentOfStudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet qui retourne les parents des élèves.
    """
    queryset = ParentOfStudent.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParentOfStudentSerializer




class ParentsOfStudentsInSchoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet qui retourne les parents des élèves inscrits dans l'école de l'utilisateur connecté.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParentOfStudentSerializer

    def get_queryset(self):
        # Supposons que l'utilisateur connecté soit lié à une école via un attribut `school_code`
        user_school = self.request.user.school_code

        # Récupérer toutes les inscriptions pour cette école qui sont actives et concernent l'année scolaire en cours
        inscriptions = Inscription.objects.filter(
            classroom__school=user_school,
            is_active=True,
            school_year__is_current_year=True
        )

        # Extraire tous les élèves inscrits
        pupils = [inscription.student for inscription in inscriptions]

        # Récupérer et retourner les parents des élèves inscrits
        parents = ParentOfStudent.objects.filter(parents_of_pupils__in=pupils).distinct()
        return parents

class PupilsViewset(viewsets.ModelViewSet):
    queryset = Pupil.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PupilSerializer
    