from rest_framework import viewsets, permissions
from backend.models.school_manager.school_manager import SchoolYear, Classroom
from api.serializers.school_manager.school_manager_serializer import SchoolYearSerializer, ClassroomSerializer


class SchoolYearViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SchoolYearSerializer

    def get_queryset(self):
        # Filtrer les années scolaires de l'école de l'utilisateur connecté
        return SchoolYear.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        # Associer l'année scolaire à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)


class ClassroomViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        # Filtrer les salles de classe par l'école de l'utilisateur connecté
        return Classroom.objects.filter(school=self.request.user.school_code)

    def perform_create(self, serializer):
        # Associer la salle de classe à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
