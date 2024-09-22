from django.db import models

# from django.forms import ValidationError

# from backend.models.admin_manager.admin_manager import SubjectGroup
# from backend.models.school_manager.school_manager import Classroom, School


# class Subject(models.Model):
#     id = models.AutoField(primary_key=True, auto_created=True)
#     name = models.CharField(max_length=50, verbose_name="Nom de la matière")
#     school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
#     group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE, verbose_name="Groupe de matière")
#     coefficient = models.IntegerField(default=1)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name = "Matière"
#         verbose_name_plural = "Matières"
#         ordering = ['name']
#         unique_together = ('name', 'group')


# class SchoolSchedule(models.Model):
#     id = models.AutoField(primary_key=True, auto_created=True)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
#     day = models.CharField(max_length=10, verbose_name="Jour")
#     start_time = models.TimeField(verbose_name="Heure de début")
#     end_time = models.TimeField(verbose_name="Heure de fin")
#     classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
#     school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
#     teacher = models.CharField(max_length=50, verbose_name="Professeur")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.subject.name} - Jour {self.day}, {self.start_time} - {self.end_time}"
    
#     class Meta:
#         verbose_name = "Calendrier scolaire"
#         verbose_name_plural = "Calendriers scolaires"
#         ordering = ['subject', 'day','start_time']
    
#     def clean(self):
#         if self.start_time >= self.end_time:
#             raise ValidationError("L'heure de début doit être antérieure à l'heure de fin.")
#         return super().clean()
    
#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)


# class SchoolCalendar(models.Model):
#     id = models.AutoField(primary_key=True, auto_created=True)
#     date = models.DateField(verbose_name="Date")
#     school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
#     events = models.TextField(verbose_name="Événements")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.date}"
    
#     class Meta:
#         verbose_name = "Calendrier scolaire"
#         verbose_name_plural = "Calendriers scolaires"
#         ordering = ['-date']
#         unique_together = ('date','school')
    
#     def clean(self):
#         if self.date < School.current_year_start:
#             raise ValidationError("La date ne peut pas être antérieure à la date de début de l'année scolaire.")
#         return super().clean()
    
#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)



# class SchoolHoliday(models.Model):
#     id = models.AutoField(primary_key=True, auto_created=True)
#     date = models.DateField(verbose_name="Date")
#     description = models.TextField(verbose_name="Description")
#     school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.date}"
    
#     class Meta:
#         verbose_name = "Congé scolaire"
#         verbose_name_plural = "Congés scolaires"
#         ordering = ['-date']
#         unique_together = ('date','school')

#     def clean(self):
#         if self.date < School.current_year_start:
#             raise ValidationError("La date ne peut pas être antérieure à la date de début de l'année scolaire.")
#         return super().clean()
    
#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)
    

# class SchoolProgram(models.Model):
#     id = models.AutoField(primary_key=True, auto_created=True)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Matière")
#     description = models.TextField(verbose_name="Description")
#     school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name="École")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.subject.name}"
    
#     class Meta:
#         verbose_name = "Programme scolaire"
#         verbose_name_plural = "Programmes scolaires"
#         ordering = ['subject']
#         unique_together = ('subject', 'school')
