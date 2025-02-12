from datetime import date
from django.db import models
from django.forms import ValidationError
from backend.models.admin_manager import SubjectGroup
from backend.models.school_manager import Classroom, School, SchoolYear


class Subject(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom de la matière")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, verbose_name="École",null=True)
    group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, verbose_name="Groupe de matière")
    coefficient = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['name']
        unique_together = ('name', 'group')


class SchoolSchedule(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
    day = models.CharField(max_length=10, verbose_name="Jour")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name="Salle de classe")
    school = models.ForeignKey(School, on_delete=models.SET_NULL, verbose_name="École",null=True)
    teacher = models.ForeignKey('backend.User', on_delete=models.CASCADE, verbose_name="Professeur")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Emplois du temps scolaire"
        verbose_name_plural = "Emplois du temps scolaires"
        ordering = ['subject', 'day', 'start_time']
        unique_together = ('subject', 'day', 'start_time', 'classroom')

    def __str__(self):
        return f"{self.subject.name} - Jour {self.day}, {self.start_time} - {self.end_time}"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("L'heure de début doit être antérieure à l'heure de fin.")

        # Vérification des chevauchements
        overlapping_schedules = SchoolSchedule.objects.filter(
            day=self.day,
            classroom=self.classroom,
            school=self.school,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )

        if overlapping_schedules.exists():
            raise ValidationError("Il y a un chevauchement avec un autre emploi du temps.")

        # Vérification que l'enseignant, la matière et la salle appartiennent à la même école
        if self.subject.school != self.school:
            raise ValidationError("La matière doit appartenir à la même école.")
        if self.classroom.school != self.school:
            raise ValidationError("La salle de classe doit appartenir à la même école.")
        if self.teacher.school_code != self.school:
            raise ValidationError("L'enseignant doit appartenir à la même école.")

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SchoolCalendar(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(verbose_name="Date")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École", null=True)
    events = models.TextField(verbose_name="Événements")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Événements du {self.date} pour {self.school}"

    class Meta:
        verbose_name = "Calendrier scolaire"
        verbose_name_plural = "Calendriers scolaires"
        ordering = ['-date']
        unique_together = ('date', 'school')

    def clean(self):
        # Remplace School.current_year_start par une logique appropriée pour obtenir la date de début
        if self.date < date.today():
            raise ValidationError("La date ne peut pas être antérieure à la date d'aujourd'hui.")
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SchoolHoliday(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    date = models.DateField(verbose_name="Date")
    description = models.TextField(verbose_name="Description")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Congé du {self.date} pour {self.school}"

    class Meta:
        verbose_name = "Congé scolaire"
        verbose_name_plural = "Congés scolaires"
        ordering = ['-date']
        unique_together = ('date', 'school')

    def clean(self):
        if self.date < date.today():
            raise ValidationError("La date ne peut pas être antérieure à la date d'aujourd'hui.")
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SchoolProgram(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
    description = models.TextField(verbose_name="Description")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Programme de {self.subject.name} pour {self.school}"

    class Meta:
        verbose_name = "Programme scolaire"
        verbose_name_plural = "Programmes scolaires"
        ordering = ['subject']
        unique_together = ('subject', 'school')

    def clean(self):
        # Vérification que la matière appartient à la même école
        if self.subject.school != self.school:
            raise ValidationError("La matière doit appartenir à la même école que le programme.")
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SchoolReportCard(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    student = models.ForeignKey('backend.User', on_delete=models.CASCADE, verbose_name="Élève")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
    grade = models.CharField(max_length=5, verbose_name="Grade")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École",null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Bulletin de {self.student.first_name} {self.student.last_name} pour {self.subject.name} ({self.grade})"
    
    class Meta:
        verbose_name = "Bulletin de notes"
        verbose_name_plural = "Bulletins de notes"
    
    def clean(self):
        # Vérification que le grade est un chiffre entre 0 et 20
        if not 0 <= int(self.grade) <= 20:
            raise ValidationError("Le grade doit être un chiffre entre 0 et 20.")
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def average_grade(self):
        # Calcul du grade moyen pour la matière
        grades = SchoolReportCard.objects.filter(student=self.student, subject=self.subject)
        return sum(int(grade.grade) for grade in grades) / len(grades) if grades else 0
    
    @property
    def is_passing(self):
        # Vérification si le grade moyen est supérieur ou égal à 10
        return self.average_grade >= 10
    
    @property
    def is_failing(self):
        # Vérification si le grade moyen est inférieur à 10
        return not self.is_passing
    
    @property
    def is_excellent(self):
        # Vérification si le grade moyen est égal à 20
        return self.average_grade == 20
    
    @property
    def is_average(self):
        # Vérification si le grade moyen est compris entre 10 et 19
        return 10 <= self.average_grade < 20
    
    @property
    def is_below_average(self):
        # Vérification si le grade moyen est inférieur à 10
        return self.average_grade < 10
    
    @property
    def grade_level(self):
        # Calcul du niveau de grade
        if self.average_grade >= 20:
            return "A"
        elif self.average_grade >= 17:
            return "B"
        elif self.average_grade >= 14:
            return "C"
        elif self.average_grade >= 11:
            return "D"
        else:
            return "F"
    
    @property
    def grade_description(self):
        # Description du grade
        if self.is_excellent:
            return "Excellent"
        elif self.is_average:
            return "Moyen"
        elif self.is_below_average:
            return "Mauvais"
        else:
            return "Très mauvais"
    
    @property
    def grade_range(self):
        # Intervalle de grade
        if self.is_excellent:
            return "20"
        elif self.is_average:
            return "17-19"
        elif self.is_below_average:
            return "14-10"
        else:
            return "F"
    
    @property
    def grade_color(self):
        # Couleur du grade
        if self.is_excellent:
            return "green"
        elif self.is_average:
            return "yellow"
        elif self.is_below_average:
            return "red"
        else:
            return "black"
    
    @property
    def grade_percentage(self):
        # Pourcentage du grade
        return (self.average_grade / 20) * 100
    
    @property
    def grade_percentage_rounded(self):
        # Pourcentage du grade arrondi
        return round(self.grade_percentage)
    
    @property
    def grade_percentage_color(self):
        # Couleur du pourcentage du grade
        if self.grade_percentage >= 90:
            return "green"
        elif self.grade_percentage >= 80:
            return "yellow"
        elif self.grade_percentage >= 70:
            return "orange"
        else:
            return "red"
    
    @property
    def grade_percentage_description(self):
        # Description du pourcentage du grade
        if self.grade_percentage >= 90:
            return "Très bien"
        elif self.grade_percentage >= 80:
            return "Bien"
        elif self.grade_percentage >= 70:
            return "Passable"
        else:
            return "Insuffisant"



class SubjectAttribution(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    teacher = models.ForeignKey('backend.User', on_delete=models.CASCADE, verbose_name="Professeur")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
    classroom = models.ForeignKey('backend.Classroom', on_delete=models.CASCADE, verbose_name="Salle de classe")
    school_year = models.ForeignKey('backend.SchoolYear', on_delete=models.CASCADE, verbose_name="Année scolaire")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject.name} ({self.classroom.name})"


    class Meta:
        verbose_name = "Attribution de matière"
        verbose_name_plural = "Attributions de matières"
        ordering = ['subject']
        unique_together = ('subject', 'classroom')
    
    def clean(self):
        # Vérification que la matière appartient à la même école que la salle de classe
        if self.subject.school != self.classroom.school:
            raise ValidationError("La matière doit appartenir à la même école que la salle de classe.")
        # Vérification que la matière n'est pas déjà attribuée à la salle de classe pour l'année scolaire en cours
        if SubjectAttribution.objects.filter(classroom=self.classroom, school_year=self.school_year).exists():
            raise ValidationError("La matière est déjà attribuée à la salle de classe pour l'année scolaire en cours.")
        
        if SubjectAttribution.objects.filter(teacher=self.teacher, subject=self.subject, classroom=self.classroom, school_year=self.school_year).exists():
            raise ValidationError("Le professeur enseigne déjà cette matière dans cette salle de classe pour l'année en cours.")

        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def classroom_teacher(self):
        # Professeur de la salle de classe
        return self.teacher.full_name()
