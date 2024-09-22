from rest_framework import serializers
from backend.models.account import TeacherSchool

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSchool
        fields = '__all__'  # Ajustez selon les champs que vous souhaitez exposer
