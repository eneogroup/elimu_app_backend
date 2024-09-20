from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from backend.models.school_manager.school_manager import School

genders = [
    ('Masculin', 'Masculin'),
    ('Féminin', 'Féminin')
]

class UserRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nom du rôle")
    permissions = models.ManyToManyField('auth.Permission', related_name='role_permissions')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Rôle"
        verbose_name_plural = "Rôles"


class UserManager(BaseUserManager):
    def create_user(self, username, password=None,):
        """
        Creates and saves a User with the given username, password.
        """
        user = self.model(username=username)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(password=password,username=username)
        user.is_admin = True
        user.save(using=self._db)
        return user


#  Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=255, unique=True,)
    
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    
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
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class StaffProfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    lastname = models.CharField(max_length=50, verbose_name="Nom", null=True, blank=True)
    firstname = models.CharField(max_length=50, verbose_name="Prénom", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=genders, verbose_name="Sexe", null=True, blank=True)
    nationality = models.CharField(max_length=50, verbose_name="Nationalité", null=True, blank=True)
    birthplace = models.CharField(max_length=100, verbose_name="Lieu de naissance", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Téléphone", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Adresse", null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    photo = models.ImageField(upload_to='staff_photos/', verbose_name="Photo", null=True, blank=True)
    skype = models.CharField(max_length=50, verbose_name="Skype", null=True, blank=True)
    gmail = models.EmailField(verbose_name="Gmail", null=True, blank=True)
    discord = models.URLField(verbose_name="Discord", null=True, blank=True)
    whatsapp = models.CharField(max_length=20, verbose_name="WhatsApp", null=True, blank=True)
    facebook = models.URLField(verbose_name="Facebook", null=True, blank=True)
    twitter = models.URLField(verbose_name="Twitter", null=True, blank=True)
    instagram = models.URLField(verbose_name="Instagram", null=True, blank=True)
    linkedin = models.URLField(verbose_name="LinkedIn", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Profil de l'utilisateur"
        verbose_name_plural = "Profils de l'utilisateurs"
    
    def __str__(self):
        return f"Profil de l'utilisateur : {self.user.username}"



