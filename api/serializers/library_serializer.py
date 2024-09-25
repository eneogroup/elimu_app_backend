from rest_framework import serializers

from backend.models.library_manager import Ebook

class EbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'
