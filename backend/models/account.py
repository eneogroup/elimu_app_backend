from django.db import models
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from backend.models.school_manager.school_manager import School, UUID4Field

genders = [
    ('Masculin', 'Masculin'),
    ('Féminin', 'Féminin')
]

class CommonProfile(models.Model):
    lastname = models.CharField(max_length=50, verbose_name="Nom", null=True, blank=True)
    firstname = models.CharField(max_length=50, verbose_name="Prénom", null=True, blank=True)
    nickname = models.CharField(max_length=50, verbose_name="Surnom", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=genders, verbose_name="Sexe", null=True, blank=True)
    nationality = models.CharField(max_length=50, verbose_name="Nationalité", null=True, blank=True)
    birthplace = models.CharField(max_length=100, verbose_name="Lieu de naissance", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Adresse", null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/', verbose_name="Photo", null=True, blank=True)
    skype = models.CharField(max_length=50, verbose_name="Skype", null=True, blank=True)
    gmail = models.EmailField(verbose_name="Gmail", null=True, blank=True)
    discord = models.URLField(verbose_name="Discord", null=True, blank=True)
    whatsapp = models.CharField(max_length=20, verbose_name="WhatsApp", null=True, blank=True)
    facebook = models.URLField(verbose_name="Facebook", null=True, blank=True)
    twitter = models.URLField(verbose_name="Twitter", null=True, blank=True)
    instagram = models.URLField(verbose_name="Instagram", null=True, blank=True)
    linkedin = models.URLField(verbose_name="LinkedIn", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du rôle")
    permissions = models.ManyToManyField('auth.Permission', related_name='role_permissions')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, verbose_name="Rôle", blank=True, null=True)
    school_code = models.ForeignKey(School, on_delete=models.SET_NULL, verbose_name="Code École", blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"Utilisateur : {self.username}"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class StaffProfile(CommonProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')

    class Meta:
        verbose_name = "Profil du personnel"
        verbose_name_plural = "Profils du personnel"

    def __str__(self):
        return f"Profil du personnel : {self.user.username}"


class ParentOfStudent(CommonProfile):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='account_of_parent', blank=True, null=True)
    profession = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = "Parent d'élève"
        verbose_name_plural = "Parents d'élèves"

    def __str__(self):
        return f"Parent : {self.lastname} {self.firstname}"



class Pupil(CommonProfile):
    id = models.AutoField(primary_key=True)
    matricule = UUID4Field(auto_created=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='pupil_profile', null=True, blank=True)
    parents = models.ManyToManyField(ParentOfStudent, related_name='parents_of_pupils')
    

    class Meta:
        verbose_name = "Élève"
        verbose_name_plural = "Élèves"

    def __str__(self):
        return f"Élève : {self.lastname} {self.firstname}"

    def clean(self):
        if self.parents.count() < 1 or self.parents.count() > 2:
            raise ValidationError('Un élève doit avoir au moins un parent et au maximum deux parents.')

    def display_parents(self):
        return ", ".join(str(parent) for parent in self.parents.all())
    display_parents.short_description = 'Parents'

# Signal to validate the number of parents
def validate_parents(sender, **kwargs):
    if kwargs['instance'].parents.count() < 1 or kwargs['instance'].parents.count() > 2:
        raise ValidationError('Un élève doit avoir au moins un parent et au maximum deux parents.')

# Connect the signal
m2m_changed.connect(validate_parents, sender=Pupil.parents.through)

class TeacherSchool(CommonProfile):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    school_code = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École", related_name='teacher_school')
    is_principal = models.BooleanField(verbose_name="Est principal", default=False)
    is_assistant = models.BooleanField(verbose_name="Est assistant", default=False)
    subjects = models.ManyToManyField('Subject', related_name='teachers', verbose_name="Matières enseignées", blank=True)
    hire_date = models.DateField(verbose_name="Date de début d'emploi", null=True, blank=True)
    phone_work = models.CharField(max_length=20, verbose_name="Téléphone professionnel", null=True, blank=True)

    class Meta:
        verbose_name = "Professeur de l'école"
        verbose_name_plural = "Professeurs de l'école"
    
    def __str__(self):
        return f"Professeur de l'école : {self.user.username}"

    def clean(self):
        if self.school_code is None:
            raise ValidationError('Un professeur doit appartenir à une école.')
        if self.school_code.is_closed:
            raise ValidationError('L\'école est fermée.')
        
        # Vérification que toutes les matières appartiennent à la même école
        for subject in self.subjects.all():
            if subject.school != self.school_code:
                raise ValidationError(f'La matière "{subject.name}" n\'appartient pas à l\'école de l\'enseignant.')

        # Vérification des matières
        if not self.subjects.exists():
            raise ValidationError('Un professeur doit enseigner au moins une matière.')


