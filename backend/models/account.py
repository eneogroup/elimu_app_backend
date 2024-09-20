from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

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
    

