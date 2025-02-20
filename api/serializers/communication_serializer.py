from rest_framework import serializers
from backend.models import Information
from backend.models.admin_manager import Tag
from backend.models.communication_manager import Announcement, Event, Message

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'content', 'recipient', 'sender', 'is_read', 'date_created']

class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'recipient']

class ReplyMessageSerializer(serializers.Serializer):
    content = serializers.CharField()
