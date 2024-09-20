from typing import Any
from django.db import models

class SchoolCycle(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom du cycle scolaire")
    description = models.TextField(verbose_name="Description du cycle scolaire", blank=True, null=True)
    
    def __str__(self):
        return self.name


class SchoolSeries(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom de la série")
    
    def __str__(self):
        return self.name


class LevelScolaship(models.Model):
    name = models.CharField(max_length=25, verbose_name="Nom du niveau")
    series = models.ForeignKey(SchoolSeries, on_delete=models.CASCADE, verbose_name="Série", blank=True, null=True)
    cycle = models.ForeignKey(SchoolCycle, on_delete=models.CASCADE, verbose_name="Cycle scolaire")
    
    def __str__(self):
        return self.name

    
    
