from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
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


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Valider que l'email existe dans le système
        try:
            form = PasswordResetForm(data=self.initial_data)
            if form.is_valid():
                return value
            else:
                raise serializers.ValidationError("Cet email n'existe pas.")
        except Exception as e:
            raise serializers.ValidationError(str(e))


    def save(self, request):
        # Envoi de l'email avec le lien de réinitialisation
        form = PasswordResetForm(data=self.validated_data)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='registration/password_reset_email.html',
                from_email='no-reply@monapp.com',
                subject_template_name='registration/password_reset_subject.txt'
            )


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    re_new_password = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)
    uid = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['re_new_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def save(self):
        try:
            uid = self.validated_data['uid']
            token = self.validated_data['token']
            new_password = self.validated_data['new_password']
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
            else:
                raise serializers.ValidationError("Token invalide ou expiré.")
        except User.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable.")


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