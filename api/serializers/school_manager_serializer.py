from rest_framework import serializers
from backend.models.account import User
from backend.models.school_manager import School, SchoolGeneralConfig, UserRegistration, SchoolAbsence, SchoolYear, Classroom, StudentEvaluation


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = ['id', 'year', 'is_current_year', 'start_date', 'end_date']

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'


class InscriptionSerializer(serializers.ModelSerializer):
    #student = PupilSerializer(read_only=True)
    class Meta:
        model = UserRegistration
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

    # def validate(self, attrs):
    #     student = attrs.get('student')
    #     school_year = attrs.get('school_year')
    #     classroom = attrs.get('classroom')

    #     # Vérification que l'élève n'est pas déjà inscrit dans cette école pour la même année scolaire
    #     existing_inscription = Inscription.objects.filter(
    #         student=student,
    #         school_year=school_year,
    #         classroom__school=classroom.school
    #     ).exists()

    #     if existing_inscription:
    #         raise serializers.ValidationError("L'élève est déjà inscrit dans cette école pour l'année scolaire sélectionnée.")

    #     # Vérification pour s'assurer que l'élève appartient à la même école que la salle de classe
    #     if student__school_code != classroom.school:
    #         raise serializers.ValidationError("L'élève doit appartenir à la même école que la salle de classe.")

    #     return super().validate(attrs)

class StudentEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEvaluation
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

    def validate(self, attrs):
        inscription = attrs.get('inscription')
        student = attrs.get('student')
        school_year = attrs.get('school_year')

        # Vérifie que l'inscription est active
        if not inscription.is_active:
            raise serializers.ValidationError("L'inscription doit être active pour enregistrer une évaluation.")

        # Vérifie que l'élève de l'inscription correspond à l'élève de l'évaluation
        if inscription.student != student:
            raise serializers.ValidationError("L'élève de l'évaluation doit correspondre à l'élève de l'inscription.")

        # Vérifie que l'année scolaire de l'inscription correspond à l'année scolaire de l'évaluation
        if inscription.school_year != school_year:
            raise serializers.ValidationError("L'année scolaire de l'inscription doit correspondre à l'année scolaire de l'évaluation.")

        return super().validate(attrs)


class SchoolAbsenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolAbsence
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    school_year = serializers.PrimaryKeyRelatedField(queryset=SchoolYear.objects.all())
    classroom = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    children = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True, required=False)

    class Meta:
        model = UserRegistration
        fields = [
            'id', 'user', 'school', 'school_year', 'classroom', 'is_paid', 'is_active', 'is_graduated', 
            'is_transferred', 'is_suspended', 'is_withdrawn', 'is_reinscribed', 'children', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        """
        Vérifie que l'utilisateur n'est pas déjà inscrit avec le même rôle pour la même année scolaire et salle de classe.
        """
        user = data.get('user')
        school_year = data.get('school_year')
        classroom = data.get('classroom')

        if UserRegistration.objects.filter(user=user, school_year=school_year, classroom=classroom).exists():
            raise serializers.ValidationError("L'utilisateur est déjà inscrit avec ce rôle pour cette année scolaire et salle de classe.")

        return data


class SchoolGeneralConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolGeneralConfig
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']