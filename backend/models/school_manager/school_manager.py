from django.db import models

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
    