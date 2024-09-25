import os
from django.db import models
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
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
    

class Information(models.Model):
    name = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='information_images', blank=True)
    slug = models.SlugField(unique=True)
    published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    # Ajout des tags
    tags = models.ManyToManyField('Tag', blank=True, related_name='informations')
    author = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey('backend.School', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return f'/information/{self.slug}'
    
    def update_views(self):
        self.views += 1
        self.save()
    
    def __str__(self):
        return self.name[:50] + '...' if len(self.name) > 50 else self.name
    
    def save_image_to_storage(self):
        self.image.storage.save(self.image.name, self.image)
        self.image = os.path.join('information_images', self.image.name)
        self.save()
        self.image.storage.delete(self.image.name)
        self.save_image_to_storage()  # Save again to generate a new filename if necessary
    
    def save_image(self, filename):
        ext = filename.split('.')[-1]
        new_filename = '{}.{}'.format(slugify(self.name), ext)
        self.image.save(new_filename, self.image, save=False)
        self.image = os.path.join('information_images', new_filename)
        self.save_image_to_storage()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    
    class Meta:
        verbose_name = 'Information'
        verbose_name_plural = 'Informations'
        ordering = ['-date_created']



class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images', blank=True)
    slug = models.SlugField(unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True, related_name='events')
    author = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey('backend.School', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return f'/evenement/{self.slug}'
    
    def update_views(self):
        self.views += 1
        self.save()
    
    def __str__(self):
        return self.name[:50] + '...' if len(self.name) > 50 else self.name
    
    def save_image_to_storage(self):
        self.image.storage.save(self.image.name, self.image)
        self.image = os.path.join('event_images', self.image.name)
        self.save()
        self.image.storage.delete(self.image.name)
        self.save_image_to_storage()  # Save again to generate a new filename if necessary
    
    def save_image(self, filename):
        ext = filename.split('.')[-1]
        new_filename = '{}.{}'.format(slugify(self.name), ext)
        self.image.save(new_filename, self.image, save=False)
        self.image = os.path.join('event_images', new_filename)
        self.save_image_to_storage()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Événement'
        verbose_name_plural = 'Événements'
        ordering = ['-start_date']

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='announcement_images', blank=True)
    slug = models.SlugField(unique=True)
    published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('Tag', blank=True, related_name='announcements')
    author = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True, blank=True)
    school = models.ForeignKey('backend.School', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return f'/annonce/{self.slug}'
    
    def update_views(self):
        self.views += 1
        self.save()
    
    def __str__(self):
        return self.title[:50] + '...' if len(self.title) > 50 else self.title
    
    def save_image_to_storage(self):
        self.image.storage.save(self.image.name, self.image)
        self.image = os.path.join('announcement_images', self.image.name)
        self.save()
        self.image.storage.delete(self.image.name)
        self.save_image_to_storage()  # Save again to generate a new filename if necessary
        
    def save_image(self, filename):
        ext = filename.split('.')[-1]
        new_filename = '{}.{}'.format(slugify(self.title), ext)
        self.image.save(new_filename, self.image, save=False)
        self.image = os.path.join('announcement_images', new_filename)
        self.save_image_to_storage()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
        ordering = ['-date_created']

# class Question(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     slug = models.SlugField(unique=True)
#     published = models.BooleanField(default=True)
#     views = models.PositiveIntegerField(default=0)
#     author = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True, blank=True)
#     school = models.ForeignKey('backend.School', on_delete=models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)
    
#     def get_absolute_url(self):
#         return f'/question/{self.slug}'
    
#     def update_views(self):
#         self.views += 1
#         self.save()
    
#     def __str__(self):
#         return self.title[:50] + '...' if len(self.title) > 50 else self.title
    
#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)
#         super().save(*args, **kwargs)
    
#     class Meta:
#         verbose_name = 'Question'
#         verbose_name_plural = 'Questions'
#         ordering = ['-date_created']

# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     content = models.TextField()
#     author = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f'Réponse de {self.author.get_full_name()[:50]}...' if self.author else 'Réponse anonyme...'
    
#     class Meta:
#         verbose_name = 'Réponse'
#         verbose_name_plural = 'Réponses'


# class Comment(models.Model):
#     content = models.TextField()
#     author = models.ForeignKey('backend.User', on_delete=models.SET_NULL, null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#     post = models.ForeignKey(
#         'Information', 'Event', 'Announcement', 'Question', on_delete=models.CASCADE
#     )
    
#     def __str__(self):
#         return f'Commentaire de {self.author.get_full_name()[:50]}...' if self.author else 'Commentaire anonyme...'

#     class Meta:
#         verbose_name = 'Commentaire'
#         verbose_name_plural = 'Commentaires'