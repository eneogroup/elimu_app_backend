from rest_framework import serializers
from backend.models.admin_manager import SchoolCycle, SchoolSeries, SchoolLevel, SubjectGroup, DocumentType, SanctionOrAppreciationType

class SchoolCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCycle
        fields = '__all__'

class SchoolSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSeries
        fields = '__all__'

class SchoolLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolLevel
        fields = '__all__'

class SubjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroup
        fields = '__all__'

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'

class SanctionOrAppreciationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SanctionOrAppreciationType
        fields = '__all__'
