from datetime import date
from django.db import models
from django.forms import ValidationError
from backend.models.account import TeacherSchool
from backend.models.admin_manager import SubjectGroup
from backend.models.school_manager import Classroom, School


class Subject(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom de la matière")
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
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
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
    teacher = models.ForeignKey(TeacherSchool, on_delete=models.CASCADE, verbose_name="Professeur")

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
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
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
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
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
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
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
