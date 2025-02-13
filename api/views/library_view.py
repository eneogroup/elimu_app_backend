from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from api.serializers.library_serializer import EbookSerializer, MaterialRequestSerializer, SchoolMaterialSerializer
from backend.constant import get_user_school
from backend.models.library_manager import Ebook, MaterialRequest, SchoolMaterial
from backend.permissions.permission_app import IsDirector, IsManager


class EbookViewSet(viewsets.ModelViewSet):
    """
    EbookViewSet is a viewset for handling CRUD operations on Ebook objects. It ensures that the operations are restricted to the school of the authenticated user.
    Attributes:
        serializer_class (EbookSerializer): The serializer class used for Ebook objects.
        permission_classes (list): List of permission classes that the user must pass to access the viewset.
    Methods:
        get_queryset(self):
            Returns a queryset of Ebook objects filtered by the school of the authenticated user.
        perform_create(self, serializer):
            Associates the created Ebook with the school of the authenticated user.
        create(self, request, *args, **kwargs):
            Customizes the creation process to include the school of the authenticated user.
        update(self, request, *args, **kwargs):
            Updates an Ebook object if it belongs to the school of the authenticated user. Returns a 403 Forbidden response if the user tries to update an Ebook from a different school.
        destroy(self, request, *args, **kwargs):
            Deletes an Ebook object if it belongs to the school of the authenticated user. Returns a 403 Forbidden response if the user tries to delete an Ebook from a different school.
    """
    serializer_class = EbookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filtrer les livres par l'école de l'utilisateur connecté
        return Ebook.objects.filter(school=get_user_school(self.request))
    
    def perform_create(self, serializer):
        # Associer le livre à l'école de l'utilisateur connecté
        serializer.save(school=get_user_school(self.request))
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier ce livre."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer ce livre."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class SchoolMaterialViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing school materials.
    This ViewSet provides the following actions:
    - list: Retrieve a list of school materials associated with the user's school.
    - retrieve: Retrieve a specific school material.
    - create: Create a new school material and associate it with the user's school.
    - update: Update an existing school material if it belongs to the user's school.
    - partial_update: Partially update an existing school material if it belongs to the user's school.
    - destroy: Delete an existing school material if it belongs to the user's school.
    Attributes:
        serializer_class (SchoolMaterialSerializer): The serializer class used for serializing and deserializing school materials.
        permission_classes (list): The list of permission classes that determine access control for the viewset.
    Methods:
        get_queryset(self):
            Returns the queryset of school materials filtered by the user's school.
        perform_create(self, serializer):
            Associates the new school material with the user's school before saving.
        create(self, request, *args, **kwargs):
            Customizes the creation process to include the user's school.
        update(self, request, *args, **kwargs):
            Updates an existing school material if it belongs to the user's school.
        destroy(self, request, *args, **kwargs):
            Deletes an existing school material if it belongs to the user's school.
    """
    serializer_class = SchoolMaterialSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager, IsDirector]
    
    def get_queryset(self):
        # Filtrer les matériels par l'école de l'utilisateur connecté
        return SchoolMaterial.objects.filter(school=get_user_school(self.request))
    
    def perform_create(self, serializer):
        # Associer le matériel à l'école de l'utilisateur connecté
        serializer.save(school=get_user_school(self.request))
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier ce matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer ce matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class MaterialRequestViewSet(viewsets.ModelViewSet):
    """
    MaterialRequestViewSet is a viewset for handling material requests in the application.
    Attributes:
        serializer_class (MaterialRequestSerializer): The serializer class used for material requests.
        permission_classes (list): The list of permission classes required to access this viewset.
    Methods:
        get_queryset(self):
            Returns the queryset of material requests filtered by the school of the logged-in user.
        perform_create(self, serializer):
            Associates the material request with the school of the logged-in user and saves the serializer.
        create(self, request, *args, **kwargs):
            Customizes the creation process to include the school of the logged-in user.
        update(self, request, *args, **kwargs):
            Updates a material request if it belongs to the school of the logged-in user. Returns a 403 Forbidden response if the user is not allowed to update the request.
        destroy(self, request, *args, **kwargs):
            Deletes a material request if it belongs to the school of the logged-in user. Returns a 403 Forbidden response if the user is not allowed to delete the request.
    """
    serializer_class = MaterialRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsManager, IsDirector]
    
    def get_queryset(self):
        # Filtrer les demandes de matériels par l'école de l'utilisateur connecté
        return MaterialRequest.objects.filter(material__school=get_user_school(self.request))
    
    def perform_create(self, serializer):
        # Associer la demande de matériel à l'école de l'utilisateur connecté
        serializer.save(requester=self.request.user, material__school=get_user_school(self.request))
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.material.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier cette demande de matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.material.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer cette demande de matériel."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)