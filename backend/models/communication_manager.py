import os
from django.db import models
from django.utils.text import slugify
from django.core.files.storage import default_storage
from django.utils.crypto import get_random_string

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
        """
        Sauvegarde l'image dans le stockage de fichiers et renomme avec un nouveau nom unique basé sur `self.name`.
        """
        if not self.image:
            return  # Si aucune image n'est présente, on ne fait rien

        # Extraire l'extension de l'image
        ext = self.image.name.split('.')[-1]
        new_filename = f"{slugify(self.name)}.{ext}"
        new_filepath = os.path.join('information_images', new_filename)

        # Si un fichier avec ce nom existe déjà, générer un nouveau nom
        if default_storage.exists(new_filepath):
            unique_suffix = get_random_string(length=8)  # Génère un suffixe unique
            new_filename = f"{slugify(self.name)}_{unique_suffix}.{ext}"
            new_filepath = os.path.join('information_images', new_filename)

        # Sauvegarder l'image avec le nouveau nom
        with default_storage.open(new_filepath, 'wb+') as destination:
            for chunk in self.image.chunks():
                destination.write(chunk)

        # Mettre à jour l'image avec le nouveau chemin
        self.image.name = new_filepath
        self.save()  # Sauvegarder l'instance pour enregistrer le chemin modifié

    def save(self, *args, **kwargs):
        """
        Override de la méthode save pour gérer la sauvegarde d'image.
        """
        super().save(*args, **kwargs)  # Appel de la méthode save parente
        self.save_image_to_storage()  # Appeler la méthode qui gère la sauvegarde de l'image
        
    
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
        """
        Sauvegarde l'image dans le stockage de fichiers et renomme avec un nouveau nom unique basé sur `self.name`.
        """
        if not self.image:
            return  # Si aucune image n'est présente, on ne fait rien

        # Extraire l'extension de l'image
        ext = self.image.name.split('.')[-1]
        new_filename = f"{slugify(self.name)}.{ext}"
        new_filepath = os.path.join('event_images', new_filename)

        # Si un fichier avec ce nom existe déjà, générer un nouveau nom
        if default_storage.exists(new_filepath):
            unique_suffix = get_random_string(length=8)  # Génère un suffixe unique
            new_filename = f"{slugify(self.name)}_{unique_suffix}.{ext}"
            new_filepath = os.path.join('event_images', new_filename)

        # Sauvegarder l'image avec le nouveau nom
        with default_storage.open(new_filepath, 'wb+') as destination:
            for chunk in self.image.chunks():
                destination.write(chunk)

        # Mettre à jour l'image avec le nouveau chemin
        self.image.name = new_filepath
        self.save()  # Sauvegarder l'instance pour enregistrer le chemin modifié

    def save(self, *args, **kwargs):
        """
        Override de la méthode save pour gérer la sauvegarde d'image.
        """
        super().save(*args, **kwargs)  # Appel de la méthode save parente
        self.save_image_to_storage()  # Appeler la méthode qui gère la sauvegarde de l'image
    
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
        """
        Sauvegarde l'image dans le stockage de fichiers et renomme avec un nouveau nom unique basé sur `self.name`.
        """
        if not self.image:
            return  # Si aucune image n'est présente, on ne fait rien

        # Extraire l'extension de l'image
        ext = self.image.name.split('.')[-1]
        new_filename = f"{slugify(self.name)}.{ext}"
        new_filepath = os.path.join('announcement_images', new_filename)

        # Si un fichier avec ce nom existe déjà, générer un nouveau nom
        if default_storage.exists(new_filepath):
            unique_suffix = get_random_string(length=8)  # Génère un suffixe unique
            new_filename = f"{slugify(self.name)}_{unique_suffix}.{ext}"
            new_filepath = os.path.join('announcement_images', new_filename)

        # Sauvegarder l'image avec le nouveau nom
        with default_storage.open(new_filepath, 'wb+') as destination:
            for chunk in self.image.chunks():
                destination.write(chunk)

        # Mettre à jour l'image avec le nouveau chemin
        self.image.name = new_filepath
        self.save()  # Sauvegarder l'instance pour enregistrer le chemin modifié

    def save(self, *args, **kwargs):
        """
        Override de la méthode save pour gérer la sauvegarde d'image.
        """
        super().save(*args, **kwargs)  # Appel de la méthode save parente
        self.save_image_to_storage()  # Appeler la méthode qui gère la sauvegarde de l'image
    
    class Meta:
        verbose_name = 'Annonce'
        verbose_name_plural = 'Annonces'
        ordering = ['-date_created']


class Message(models.Model):
    content = models.TextField(verbose_name='Contenu')
    recipient = models.ForeignKey('backend.User', on_delete=models.CASCADE, related_name='received_messages')
    sender = models.ForeignKey('backend.User', on_delete=models.CASCADE, related_name='sent_messages')
    is_read = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message de {self.sender} à {self.recipient}'
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-date_created']
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    def mark_as_unread(self):
        self.is_read = False
        self.save()
    
    def delete_message(self):
        self.delete()
    
    def send_reply(self, content):
        new_message = Message.objects.create(content=content, recipient=self.sender, sender=self.recipient)
        return new_message
    
    def get_replies(self):
        return Message.objects.filter(recipient=self.sender, sender=self.recipient).order_by('-date_created')
    


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