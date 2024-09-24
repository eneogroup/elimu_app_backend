from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models.account import ParentOfStudent, Pupil, TeacherSchool
from api.serializers.account_serializer import ParentOfStudentSerializer, PupilSerializer, TeacherSerializer
from rest_framework import status

from backend.models.school_manager.school_manager import Inscription


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