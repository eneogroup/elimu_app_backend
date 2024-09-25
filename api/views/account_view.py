from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models.account import ParentOfStudent, Pupil, TeacherSchool, User
from api.serializers.account_serializer import ParentOfStudentSerializer, PupilSerializer, TeacherSerializer, UserSerializer
from rest_framework import status

from backend.models.school_manager import Inscription
from backend.permissions.permission_app import IsManager, IsDirector

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]  # Les utilisateurs doivent être authentifiés

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
    permission_classes = [permissions.IsAuthenticated]
    queryset = ParentOfStudent.objects.all()
    serializer_class = ParentOfStudentSerializer

class PupilViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Pupil.objects.all()
    serializer_class = PupilSerializer


class ParentsOfStudentsInSchoolView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Supposons que l'utilisateur connecté soit lié à une école via un attribut `school`
        user_school = request.user.school_code

        # Récupérer toutes les inscriptions pour cette école
        inscriptions = Inscription.objects.filter(classroom__school=user_school, is_active=True, school_year__is_current_year=True)

        # Extraire tous les élèves inscrits
        pupils = [inscription.student for inscription in inscriptions]

        # Récupérer tous les parents des élèves inscrits
        parents = ParentOfStudent.objects.filter(parents_of_pupils__in=pupils).distinct()

        # Sérialiser les données des parents
        serializer = ParentOfStudentSerializer(parents, many=True)

        return Response(serializer.data)