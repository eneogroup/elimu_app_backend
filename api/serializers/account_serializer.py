from rest_framework import serializers
from backend.models.account import ParentOfStudent, Pupil, TeacherSchool

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherSchool
        fields = '__all__'  # Ajustez selon les champs que vous souhaitez exposer

class ParentOfStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentOfStudent
        fields = '__all__'  # ou spécifiez explicitement les champs

class PupilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pupil
        fields = '__all__'