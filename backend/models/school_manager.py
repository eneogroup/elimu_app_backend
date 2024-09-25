from django.db import models
from django.forms import ValidationError
from backend.models.admin_manager import SchoolLevel

cities = [
    ('Brazzaville', 'Brazzaville'),
    ('Pointe Noire', 'Pointe Noire')
]

import uuid
import hashlib

class UUID4Field(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 17)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('null', False)
        kwargs.setdefault('editable', True)
        super().__init__(*args, **kwargs)

    def generate_short_uuid(self):
        full_uuid = uuid.uuid4().hex
        short_uuid = hashlib.sha1(full_uuid.encode('utf-8')).hexdigest()[:15]
        return short_uuid

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname, None)
        if not value:
            value = self.generate_short_uuid()
            setattr(model_instance, self.attname, value)
        return value

class School(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    code = UUID4Field(auto_created=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Nom d'école")
    address = models.CharField(max_length=200, verbose_name="Adresse")
    city = models.CharField(max_length=100, verbose_name="Ville", choices=cities)
    postal_code = models.CharField(max_length=10, verbose_name="Code postal", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True, null=True)
    website = models.URLField(verbose_name="Site web", max_length=200, blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", verbose_name="Logo", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "École"
        verbose_name_plural = "Écoles"

class SchoolYear(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
    year = models.CharField(max_length=20, verbose_name="Année scolaire")
    is_current_year = models.BooleanField(default=False, verbose_name="Année en cours")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(verbose_name="Date de fin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    def __str__(self):
        return f"{self.year} - {self.school.name}"
    
    class Meta:
        verbose_name = "Année scolaire"
        verbose_name_plural = "Années scolaires"
    
    def get_current_year(self):
        from.school_manager import SchoolYear
        current_year = SchoolYear.objects.filter(school=self.school, is_current_year=True).first()
        return current_year.year if current_year else None
    
    def get_current_school_year(self):
        from .school_manager import SchoolYear
        current_school_year = SchoolYear.objects.filter(school=self.school, is_current_year=True).first()
        return current_school_year


class Classroom(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
    name = models.CharField(max_length=100, verbose_name="Nom de la salle")
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE, verbose_name="Niveau scolaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    def __str__(self):
        return f"{self.name} - {self.school_level.name}"
    
    class Meta:
        verbose_name = "Salle de classe"
        verbose_name_plural = "Salles de classes"


class Inscription(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    student = models.ForeignKey("backend.Pupil", on_delete=models.CASCADE, verbose_name="Élève")
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, verbose_name="Année scolaire")
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name="Salle de classe")

    # Statut
    is_paid = models.BooleanField(default=False, verbose_name="Payé")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    is_graduated = models.BooleanField(default=False, verbose_name="Élève admis(e)")
    is_transferred = models.BooleanField(default=False, verbose_name="Élève transféré(e)")
    is_suspended = models.BooleanField(default=False, verbose_name="Élève suspendu(e)")
    is_withdrawn = models.BooleanField(default=False, verbose_name="Élève retiré(e)")
    is_reinscribed = models.BooleanField(default=False, verbose_name="Élève réinscrit(e)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Inscription"
        verbose_name_plural = "Inscriptions"
        unique_together = ('student', 'classroom', 'school_year')  # Un élève ne peut pas être inscrit plusieurs fois dans la même salle de classe pour la même année scolaire

    def __str__(self):
        return f"{self.student.firstname} {self.student.lastname} - {self.school_year.year}"

    def clean(self):
        # # Vérification pour s'assurer que l'élève appartient à la même école que la salle de classe
        # if self.student.school_code != self.classroom.school:
        #     raise ValidationError("L'élève doit appartenir à la même école que la salle de classe.")
        
        # Vérifier que l'élève n'est pas déjà inscrit dans cette école pour la même année scolaire
        existing_inscription = Inscription.objects.filter(
            student=self.student,
            school_year=self.school_year,
            classroom__school=self.classroom.school
        ).exists()
        
        if existing_inscription:
            raise ValidationError("L'élève est déjà inscrit dans cette école pour l'année scolaire sélectionnée.")
        
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # Valide les données avant la sauvegarde
        super().save(*args, **kwargs)

    def get_student_name(self):
        return f"{self.student.firstname} {self.student.lastname}"

class StudentEvaluation(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    student = models.ForeignKey("backend.Pupil", on_delete=models.CASCADE, verbose_name="Élève")
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, verbose_name="Inscription")
    school_year = models.ForeignKey(SchoolYear, on_delete=models.CASCADE, verbose_name="Année scolaire")
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name="Matière")  # Ajuste le chemin selon ton modèle
    evaluation_date = models.DateField(verbose_name="Date de l'évaluation")
    score = models.FloatField(verbose_name="Score", null=True, blank=True)
    remarks = models.TextField(verbose_name="Remarques", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Évaluation d'élève"
        verbose_name_plural = "Évaluations d'élèves"
        unique_together = ('student', 'subject', 'evaluation_date')  # Un élève ne peut pas avoir deux évaluations pour la même matière le même jour

    def __str__(self):
        return f"Évaluation de {self.student.firstname} {self.student.lastname} - {self.subject.name}"

    def clean(self):
        # Vérifie que l'inscription est active
        if not self.inscription.is_active:
            raise ValidationError("L'inscription doit être active pour enregistrer une évaluation.")
        
        # Vérifie que l'élève de l'inscription correspond à l'élève de l'évaluation
        if self.inscription.student != self.student:
            raise ValidationError("L'élève de l'évaluation doit correspondre à l'élève de l'inscription.")
        
        # Vérifie que l'année scolaire de l'inscription correspond à l'année scolaire de l'évaluation
        if self.inscription.school_year != self.school_year:
            raise ValidationError("L'année scolaire de l'inscription doit correspondre à l'année scolaire de l'évaluation.")
        
        return super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)