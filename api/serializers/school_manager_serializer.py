from rest_framework import serializers
from backend.models.school_manager import Inscription, SchoolYear, Classroom, StudentEvaluation


class SchoolYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = '__all__'

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = '__all__'


class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

    def validate(self, attrs):
        student = attrs.get('student')
        school_year = attrs.get('school_year')
        classroom = attrs.get('classroom')

        # Vérification que l'élève n'est pas déjà inscrit dans cette école pour la même année scolaire
        existing_inscription = Inscription.objects.filter(
            student=student,
            school_year=school_year,
            classroom__school=classroom.school
        ).exists()

        if existing_inscription:
            raise serializers.ValidationError("L'élève est déjà inscrit dans cette école pour l'année scolaire sélectionnée.")

        # Vérification pour s'assurer que l'élève appartient à la même école que la salle de classe
        if student.school_code != classroom.school:
            raise serializers.ValidationError("L'élève doit appartenir à la même école que la salle de classe.")

        return super().validate(attrs)

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