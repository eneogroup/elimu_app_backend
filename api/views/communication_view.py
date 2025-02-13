from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from api.serializers.communication_serializer import AnnouncementSerializer, CreateMessageSerializer, EventSerializer, InformationSerializer, MessageSerializer, ReplyMessageSerializer, TagSerializer
from backend.constant import get_user_school
from backend.models.admin_manager import Tag
from backend.models.communication_manager import Announcement, Event, Information, Message
from django.core.exceptions import ObjectDoesNotExist

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class InformationViewSet(viewsets.ModelViewSet):
    serializer_class = InformationSerializer
    permission_classes = [permissions.IsAuthenticated,]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['-date_created']
    
    def get_queryset(self):
        # Filtrer les informations par l'école de l'utilisateur connecté
        return Information.objects.filter(school=get_user_school(self.request))
    
    def perform_create(self, serializer):
        school = get_user_school(self.request)
        if not school:
            return Response({"detail": "École non trouvée."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(school=school)
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette Information."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette Information."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']
    
    def get_queryset(self):
        # Filtrer les événements par l'école de l'utilisateur connecté
        return Event.objects.filter(school=get_user_school(self.request))
    
    def perform_create(self, serializer):
        # Associer l'événement à l'école de l'utilisateur connecté
        serializer.save(school=get_user_school(self.request))
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cet Événement."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cet Événement."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['title']
    ordering_fields = ['title']
    
    def get_queryset(self):
        # Filtrer les annonces par l'école de l'utilisateur connecté
        return Announcement.objects.filter(school=get_user_school(self.request))
    
    def perform_create(self, serializer):
        # Associer l'annonce à l'école de l'utilisateur connecté
        serializer.save(school=get_user_school(self.request))
    
    def create(self, request, *args, **kwargs):
        # Personnaliser la création pour inclure l'école de l'utilisateur
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas modifier cette Annonce."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != request.user.school_code:
            return Response({"detail": "Vous ne pouvez pas supprimer cette Annonce."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Récupère les messages reçus par l'utilisateur connecté."""
        return Message.objects.filter(recipient=self.request.user)

    def create(self, request, *args, **kwargs):
        """Permet à un utilisateur d'envoyer un message."""
        serializer = CreateMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(sender=request.user)
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marque un message comme lu."""
        message = self.get_object()
        message.mark_as_read()
        return Response({'status': 'Message marqué comme lu'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def mark_as_unread(self, request, pk=None):
        """Marque un message comme non lu."""
        message = self.get_object()
        message.mark_as_unread()
        return Response({'status': 'Message marqué comme non lu'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """Répond à un message."""
        message = self.get_object()
        serializer = ReplyMessageSerializer(data=request.data)
        if serializer.is_valid():
            reply = message.send_reply(content=serializer.validated_data['content'])
            return Response(MessageSerializer(reply).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Récupère toutes les réponses associées à ce message."""
        message = self.get_object()
        replies = message.get_replies()
        serializer = MessageSerializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def delete_message(self, request, pk=None):
        """Supprime un message."""
        message = self.get_object()
        message.delete()
        return Response({'status': 'Message supprimé'}, status=status.HTTP_204_NO_CONTENT)

