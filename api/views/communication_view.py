from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions

from api.serializers.communication_serializer import AnnouncementSerializer, EventSerializer, InformationSerializer, TagSerializer
from backend.models.communication_manager import Announcement, Event, Information, Tag

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class InformationViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['-date_created']
    
    def get_queryset(self):
        # Filtrer les informations par l'école de l'utilisateur connecté
        return Information.objects.filter(school=self.request.user.school_code)
    
    def perform_create(self, serializer):
        # Associer l'information à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cet Information."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cet v."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']
    
    def get_queryset(self):
        # Filtrer les événements par l'école de l'utilisateur connecté
        return Event.objects.filter(school=self.request.user.school_code)
    
    def perform_create(self, serializer):
        # Associer l'événement à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cet Événement."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cet événement."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title']
    ordering_fields = ['title']
    
    def get_queryset(self):
        # Filtrer les annonces par l'école de l'utilisateur connecté
        return Announcement.objects.filter(school=self.request.user.school_code)
    
    def perform_create(self, serializer):
        # Associer l'annonce à l'école de l'utilisateur connecté
        serializer.save(school=self.request.user.school_code)
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette Annonce."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school_code != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette Annonce."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
