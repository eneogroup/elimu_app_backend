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
    """
    A viewset for viewing and editing Tag instances.

    Attributes:
        queryset (QuerySet): The queryset that retrieves all Tag objects.
        serializer_class (Serializer): The serializer class used to serialize and deserialize Tag objects.
        permission_classes (list): The list of permission classes that determine access control.
        search_fields (list): The list of fields that can be searched.
        ordering_fields (list): The list of fields that can be used for ordering.
        ordering (list): The default ordering for the queryset.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

class InformationViewSet(viewsets.ModelViewSet):
    """
    InformationViewSet is a ModelViewSet for managing Information objects. It provides
    CRUD operations with custom behavior to ensure that the operations are restricted
    to the school of the authenticated user.
    Attributes:
        serializer_class (InformationSerializer): The serializer class used for the viewset.
        permission_classes (list): List of permission classes applied to the viewset.
        search_fields (list): List of fields that can be searched.
        ordering_fields (list): List of fields that can be used for ordering.
        ordering (list): Default ordering for the queryset.
    Methods:
        get_queryset(self):
            Returns the queryset filtered by the school of the authenticated user.
        perform_create(self, serializer):
            Saves the serializer with the school of the authenticated user. Returns a
            response with an error message if the school is not found.
        create(self, request, *args, **kwargs):
            Customizes the creation process to include the school of the authenticated user.
        update(self, request, *args, **kwargs):
            Updates an Information object if it belongs to the school of the authenticated user.
            Returns a response with an error message if the user does not have permission.
        destroy(self, request, *args, **kwargs):
            Deletes an Information object if it belongs to the school of the authenticated user.
            Returns a response with an error message if the user does not have permission.
    """
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
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier cette Information."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer cette Information."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class EventViewSet(viewsets.ModelViewSet):
    """
    EventViewSet is a viewset for handling CRUD operations on Event objects. It ensures that events are filtered and associated with the school of the authenticated user.
    Attributes:
        serializer_class (EventSerializer): The serializer class used for Event objects.
        permission_classes (list): List of permission classes that the user must pass to access the viewset.
        search_fields (list): List of fields that can be searched.
        ordering_fields (list): List of fields that can be used for ordering.
    Methods:
        get_queryset(self):
            Returns a queryset of Event objects filtered by the school of the authenticated user.
        perform_create(self, serializer):
            Associates the created event with the school of the authenticated user.
        create(self, request, *args, **kwargs):
            Customizes the creation process to include the school of the authenticated user.
        update(self, request, *args, **kwargs):
            Updates an event if it belongs to the school of the authenticated user. Returns a 403 response if the user tries to update an event from a different school.
        destroy(self, request, *args, **kwargs):
            Deletes an event if it belongs to the school of the authenticated user. Returns a 403 response if the user tries to delete an event from a different school.
    """
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
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier cet Événement."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer cet Événement."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Announcements.
    This ViewSet provides the following functionalities:
    - List, retrieve, create, update, and delete Announcements.
    - Filter Announcements by the school of the authenticated user.
    - Ensure that Announcements are associated with the school of the authenticated user.
    Attributes:
        serializer_class (AnnouncementSerializer): The serializer class used for Announcement objects.
        permission_classes (list): List of permission classes that the user must pass to access the view.
        search_fields (list): List of fields that can be searched.
        ordering_fields (list): List of fields that can be used for ordering.
    Methods:
        get_queryset(self):
            Returns the queryset of Announcements filtered by the school of the authenticated user.
        perform_create(self, serializer):
            Associates the Announcement with the school of the authenticated user before saving.
        create(self, request, *args, **kwargs):
            Customizes the creation process to include the school of the authenticated user.
        update(self, request, *args, **kwargs):
            Updates an Announcement if it belongs to the school of the authenticated user.
            Returns a 403 Forbidden response if the user tries to update an Announcement from a different school.
        destroy(self, request, *args, **kwargs):
            Deletes an Announcement if it belongs to the school of the authenticated user.
            Returns a 403 Forbidden response if the user tries to delete an Announcement from a different school.
    """
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
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas modifier cette Annonce."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.school != get_user_school(request):
            return Response({"detail": "Vous ne pouvez pas supprimer cette Annonce."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    """
    MessageViewSet is a viewset for handling message-related operations.

    Attributes:
        queryset (QuerySet): The queryset of all Message objects.
        serializer_class (Serializer): The serializer class for Message objects.
        permission_classes (list): The list of permission classes.

    Methods:
        get_queryset(self):
            Retrieves the messages received by the authenticated user.

        create(self, request, *args, **kwargs):
            Allows a user to send a message.

        mark_as_read(self, request, pk=None):
            Marks a message as read.

        mark_as_unread(self, request, pk=None):
            Marks a message as unread.

        reply(self, request, pk=None):
            Replies to a message.

        replies(self, request, pk=None):
            Retrieves all replies associated with a message.

        delete_message(self, request, pk=None):
            Deletes a message.
    """
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

