from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from api.serializers.library_serializer import EbookSerializer, MaterialRequestSerializer, SchoolMaterialSerializer
from backend.models.library_manager import Ebook, MaterialRequest, SchoolMaterial
from backend.permissions.permission_app import IsDirector, IsManager

class EbookViewSet(viewsets.ModelViewSet):
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
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier ce livre."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer ce livre."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class SchoolMaterialViewSet(viewsets.ModelViewSet):
    serializer_class = SchoolMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager, IsDirector]
    
    def get_queryset(self):
        # Filtrer les matériels par l'école de l'utilisateur connecté
        return SchoolMaterial.objects.filter(school=self.request.user.school_code)
    
    def perform_create(self, serializer):
        # Associer le matériel à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier ce matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer ce matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class MaterialRequestViewSet(viewsets.ModelViewSet):
    serializer_class = MaterialRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager, IsDirector]
    
    def get_queryset(self):
        # Filtrer les demandes de matériels par l'école de l'utilisateur connecté
        return MaterialRequest.objects.filter(material__school=self.request.user.school_code)
    
    def perform_create(self, serializer):
        # Associer la demande de matériel à l'école de l'utilisateur connecté
        serializer.save(requester=self.request.user, material__school=self.request.user.school_code)
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.material.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette demande de matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.material.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette demande de matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)