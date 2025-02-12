from django.forms import ValidationError
from rest_framework import serializers
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from backend.models.account import User, UserRole
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'roles', 'role_name', 'is_active', 'photo',
            'matricule', 'lastname', 'firstname', 'nickname', 'gender', 'nationality', 'birthplace', 'date_of_birth',
            'phone', 'address', 'phone_work', 'profession', 'hire_date', 'is_principal', 'is_assistant',
            'skype', 'gmail', 'discord', 'facebook', 'linkedin', 'instagram', 'twitter', 'whatsapp',
            'created_at', 'updated_at',
        ]
        extra_kwargs = {'password': {'write_only': True}}  # Empêcher l'affichage du mot de passe

    def get_role_name(self, obj):
        """ Retourne le nom du rôle de l'utilisateur """
        return obj.role.name if obj.role else None

    def validate(self, data):
        """ Vérifie que l'utilisateur a bien un rôle valide """
        role = data.get('role')
        if role and role.name.lower() not in ["teacher", "parent", "pupil"]:
            raise serializers.ValidationError("Le rôle spécifié n'est pas valide.")
        return data

    def create(self, validated_data):
        """ Assigne automatiquement le rôle basé sur la création d'un utilisateur spécifique """
        role = validated_data.get('role')
        if not role:
            raise serializers.ValidationError("Un rôle doit être attribué.")
        
        try:
            validated_data['role'] = UserRole.objects.get(name=role.name)
        except UserRole.DoesNotExist:
            raise serializers.ValidationError("Le rôle spécifié n'existe pas dans le système.")
        
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance


    def to_representation(self, instance):
        """ Afficher les champs dynamiquement selon le rôle """
        data = super().to_representation(instance)

        # Masquer les champs selon le rôle
        if instance.role.name.lower() == "teacher":
            # Cacher les champs inutiles pour un enseignant
            del data['hire_date']
            del data['phone_work']
            del data['profession']

        elif instance.role.name.lower() == "parent":
            # Cacher les champs spécifiques aux enseignants et élèves
            del data['nickname']
            del data['is_principal']
            del data['is_assistant']
        
        elif instance.role.name.lower() == "pupil":
            # Cacher les champs inutiles pour un élève
            del data['is_principal']
            del data['is_assistant']
            del data['hire_date']
            del data['phone_work']
            del data['profession']

        return data



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

