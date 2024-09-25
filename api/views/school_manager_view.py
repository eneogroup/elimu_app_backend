from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from backend.models.school_manager import Inscription, SchoolYear, Classroom, StudentEvaluation
from api.serializers.school_manager_serializer import InscriptionSerializer, SchoolYearSerializer, ClassroomSerializer, StudentEvaluationSerializer


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

class InscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InscriptionSerializer

    def get_queryset(self):
        return Inscription.objects.filter(classroom__school=self.request.user.school_code)

    def perform_create(self, serializer):
        serializer.save(classroom=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classroom.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette inscription."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classroom.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette inscription."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.classroom.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas afficher cette inscription."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class StudentEvaluationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StudentEvaluationSerializer

    def get_queryset(self):
        return StudentEvaluation.objects.filter(inscription__classroom__school=self.request.user.school_code)

    def perform_create(self, serializer):
        serializer.save(inscription=self.request.user.school_code)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.inscription.classroom.school != request.user.teacherschool.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette évaluation."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.inscription.classroom.school != request.user.teacherschool.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette évaluation."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
