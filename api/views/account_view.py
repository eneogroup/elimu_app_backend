from rest_framework import viewsets, permissions
from rest_framework.response import Response
from backend.models.account import TeacherSchool
from api.serializers.account_serializer import TeacherSerializer
from rest_framework import status


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
