from django.db import models
from django.core.exceptions import ValidationError

class Ebook(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    cover_image = models.ImageField(upload_to='cover_images')
    pdf_file = models.FileField(upload_to='pdf_files')
    school = models.ForeignKey('backend.School', on_delete=models.CASCADE, null=True)
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


class SchoolMaterial(models.Model):
    MATERIAL_TYPE_CHOICES = [
        ('livre', 'Livre'),
        ('ordinateur', 'Ordinateur'),
        ('fourniture', 'Fourniture scolaire'),
        ('autre', 'Autre'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom du matériel")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPE_CHOICES, verbose_name="Type de matériel")
    quantity = models.PositiveIntegerField(verbose_name="Quantité")
    available_quantity = models.PositiveIntegerField(verbose_name="Quantité disponible")
    school = models.ForeignKey('backend.School', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def is_available(self):
        return self.available_quantity > 0


class MaterialRequest(models.Model):
    material = models.ForeignKey(SchoolMaterial, on_delete=models.CASCADE, related_name="requests")
    requester = models.ForeignKey('backend.User', on_delete=models.CASCADE, verbose_name="Demandeur")
    request_date = models.DateField(auto_now_add=True, verbose_name="Date de demande")
    quantity_requested = models.PositiveIntegerField(verbose_name="Quantité demandée")
    status = models.CharField(max_length=20, choices=[('approuvé', 'Approuvé'), ('rejeté', 'Rejeté'), ('en attente', 'En attente')], default='en attente', verbose_name="Statut")
    approved_date = models.DateField(null=True, blank=True, verbose_name="Date d'approbation")
    rejected_reason = models.TextField(null=True, blank=True, verbose_name="Raison du rejet")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Demande de matériel'
        verbose_name_plural = 'Demandes de matériel'
        
    
    def __str__(self):
        return f"Demande de {self.requester} pour {self.material.name}"

    def approve(self):
        if self.quantity_requested <= self.material.available_quantity:
            self.material.available_quantity -= self.quantity_requested
            self.material.save()
            self.status = 'approuvé'
        else:
            raise ValidationError("Quantité demandée dépasse la quantité disponible.")

    def reject(self):
        self.status = 'rejeté'

