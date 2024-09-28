from django.db import models

class SchoolCycle(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom du cycle scolaire")
    description = models.TextField(verbose_name="Description du cycle scolaire", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Cycle scolaire"
        verbose_name_plural = "Cycles scolaires"


class SchoolSeries(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom de la série")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Série"
        verbose_name_plural = "Séries"


class SchoolLevel(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom du niveau")
    series = models.ForeignKey(SchoolSeries, on_delete=models.CASCADE, verbose_name="Série", blank=True, null=True)
    cycle = models.ForeignKey(SchoolCycle, on_delete=models.CASCADE, verbose_name="Cycle scolaire")
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Niveau scolaire"
        verbose_name_plural = "Niveaux scolaires"


class SubjectGroup(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom du groupe de matière")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Groupe de matière"
        verbose_name_plural = "Groupes de matières"


class DocumentType(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom du type de document")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Type de document"
        verbose_name_plural = "Types de documents"


class SanctionOrAppreciationType(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=50, verbose_name="Nom du type de sanction ou d'appréciation")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Type de sanction ou d'appréciation"
        verbose_name_plural = "Types de sanctions ou d'appréciations"
        ordering = ['name']


# class SanctionOrAppreciation(models.Model):
#     id = models.AutoField(primary_key=True, auto_created=True)
#     student = models.ForeignKey('backend.Pupil', on_delete=models.CASCADE, verbose_name="Étudiant")
#     subject = models.ForeignKey('backend.Subject', on_delete=models.CASCADE, verbose_name="Matière")
#     type = models.ForeignKey(SanctionOrAppreciationType, on_delete=models.CASCADE, verbose_name="Type de sanction ou d'appréciation")
#     description = models.TextField(verbose_name="Description")
#     date = models.DateField(verbose_name="Date")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.type} - {self.student}"
    
#     class Meta:
#         verbose_name = "Sanction ou appréciation"
#         verbose_name_plural = "Sanctions ou appréciations"
#         ordering = ['-created_at']
#         unique_together = ('student', 'type')