import os
from django.db import models

from django.db import models
from django.core.exceptions import ValidationError
import os

class Ebook(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='cover_images')
    pdf_file = models.FileField(upload_to='pdf_files')
    school = models.ForeignKey('backend.School', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ebook'
        verbose_name_plural = 'Ebooks'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/ebook/{self.pk}'
    
    def clean(self):
        # Vérifier que le fichier PDF est bien un PDF
        if self.pdf_file and not self.pdf_file.name.endswith('.pdf'):
            raise ValidationError("Le fichier doit être un PDF.")
        
        # Vérifier que l'image de couverture est bien une image
        if self.cover_image and not any(self.cover_image.name.endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            raise ValidationError("L'image de couverture doit être au format JPG ou PNG.")
    
    def save(self, *args, **kwargs):
        self.clean()  # Vérification des champs avant de sauvegarder
        # Modifications pour un meilleur traitement des noms de fichiers
        if self.cover_image:
            ext = self.cover_image.name.split('.')[-1]
            self.cover_image.name = f'{self.title}_cover.{ext}'
        
        if self.pdf_file:
            ext = self.pdf_file.name.split('.')[-1]
            self.pdf_file.name = f'{self.title}.{ext}'

        super().save(*args, **kwargs)



