from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions

from api.serializers.library_serializer import EbookSerializer
from backend.models.library_manager.library_manager import Ebook

class EbookViewSet(viewsets.ModelViewSet):
    queryset = Ebook.objects.all()
    serializer_class = EbookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filtrer les livres par l'école de l'utilisateur connecté
        return Ebook.objects.filter(school=self.request.user.school_code)
    
    def perform_create(self, serializer):
        # Associer le livre à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier ce livre."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer ce livre."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
