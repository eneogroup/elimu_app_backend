from rest_framework import serializers
from backend.models.subject_manager import SchoolReportCard, Subject, SchoolSchedule, SchoolCalendar, SchoolHoliday, SchoolProgram, SubjectAttribution

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

class SchoolScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSchedule
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

    def validate(self, attrs):
        # Vous pouvez inclure ici les validations personnalisées
        subject = attrs.get('subject')
        classroom = attrs.get('classroom')
        teacher = attrs.get('teacher')
        
        if subject.school != classroom.school:
            raise serializers.ValidationError("La salle de classe doit appartenir à la même école que la matière.")
        if subject.school != teacher.school_code:
            raise serializers.ValidationError("L'enseignant doit appartenir à la même école que la matière.")
        
        return super().validate(attrs)

class SchoolCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCalendar
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

class SchoolHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolHoliday
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

class SchoolProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolProgram
        fields = '__all__'  # Incluez tous les champs ou spécifiez ceux que vous voulez exposer

    def validate(self, attrs):
        subject = attrs.get('subject')
        school = attrs.get('school')
        
        if subject.school != school:
            raise serializers.ValidationError("La matière doit appartenir à la même école que le programme.")
        
        return super().validate(attrs)


class SubjectAttributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectAttribution
        fields = '__all__'


class SchoolReportCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolReportCard
        fields = '__all__'
