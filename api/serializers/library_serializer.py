from rest_framework import serializers

from backend.models.library_manager import Ebook, MaterialRequest, SchoolMaterial

class EbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ebook
        fields = '__all__'

class SchoolMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolMaterial
        fields = '__all__'

class MaterialRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialRequest
        fields = '__all__'
