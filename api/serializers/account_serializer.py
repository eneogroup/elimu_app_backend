from rest_framework import serializers
from backend.models.account import ParentOfStudent, Pupil, TeacherSchool, User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'is_admin', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


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