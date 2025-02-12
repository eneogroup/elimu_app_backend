from django.db import models
from django.db.models.signals import m2m_changed
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.forms import ValidationError
from backend.models.school_manager import School, UUID4Field

genders = [
    ('Masculin', 'Masculin'),
    ('Féminin', 'Féminin')
]

class CommonProfile(models.Model):
    matricule = UUID4Field(auto_created=True, blank=True)
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
    is_principal = models.BooleanField(verbose_name="Est principal", default=False)
    is_assistant = models.BooleanField(verbose_name="Est assistant", default=False)
    hire_date = models.DateField(verbose_name="Date de début d'emploi", null=True, blank=True)
    phone_work = models.CharField(max_length=20, verbose_name="Téléphone professionnel", null=True, blank=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du rôle")

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


class User(AbstractBaseUser, PermissionsMixin, CommonProfile):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    roles = models.ManyToManyField(UserRole, verbose_name="Rôles", blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return f"Utilisateur : {self.username}"
    
    def full_name(self):
        return f"{self.lastname} {self.firstname}" if self.lastname and self.firstname else self.username



    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
    
    def has_role(self, role_name):
        """ Vérifie si l'utilisateur a un rôle spécifique """
        return self.roles.filter(name=role_name).exists()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin




