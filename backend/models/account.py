from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


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

    is_active = models.BooleanField(default=True)
    
    is_admin = models.BooleanField(default=False)
    
    # is_admin_school = models.BooleanField(default=False)
    
    # is_manager = models.BooleanField(default=False)
    
    # is_accountant = models.BooleanField(default=False)
    
    # is_student = models.BooleanField(default=False)
    
    # is_teacher = models.BooleanField(default=False)
    
    # is_parent = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'


    def __str__(self):
        return f"Utilisateur : {self.username}"

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

