from django.db import models
from django.utils.text import slugify

class SchoolCycle(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom du cycle scolaire")
    description = models.TextField(verbose_name="Description du cycle scolaire", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Cycle scolaire"
        verbose_name_plural = "Cycles scolaires"


class SchoolSeries(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom de la série")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Série"
        verbose_name_plural = "Séries"


class SchoolLevel(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom du niveau")
    series = models.ForeignKey(SchoolSeries, on_delete=models.CASCADE, verbose_name="Série", blank=True, null=True)
    cycle = models.ForeignKey(SchoolCycle, on_delete=models.CASCADE, verbose_name="Cycle scolaire")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.name} {self.series}"
    
    class Meta:
        verbose_name = "Niveau scolaire"
        verbose_name_plural = "Niveaux scolaires"


class SubjectGroup(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom du groupe de matière")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Groupe de matière"
        verbose_name_plural = "Groupes de matières"


class DocumentType(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom du type de document")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Type de document"
        verbose_name_plural = "Types de documents"


class SanctionOrAppreciationType(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom du type de sanction ou d'appréciation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Type de sanction ou d'appréciation"
        verbose_name_plural = "Types de sanctions ou d'appréciations"
        ordering = ['name']


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/tag/{self.slug}'
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de la catégorie")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Catégorie d\'expense'
        verbose_name_plural = 'Catégories d\'expenses'
        ordering = ['name']
