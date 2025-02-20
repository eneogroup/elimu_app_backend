from django.contrib import admin
from backend.models.account import *
from backend.models.admin_manager import *
from backend.models.school_manager import *
from django.utils.html import format_html

per_page = 20

admin.site.site_header = "ELIMU - Application de gestion scolaire"
admin.site.site_title = "ELIMU - Application de gestion scolaire"
admin.site.index_title = "Bienvenue dans l'interface d'administration ELIMU"

# Register your models here.
# model from admin_manager module
@admin.register(SchoolCycle)
class SchoolCycleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name',)
    ordering = ('id',)
    list_per_page = per_page
    
@admin.register(SchoolSeries)
class SchoolSeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name',)
    ordering = ('id',)
    list_per_page = per_page

@admin.register(SchoolLevel)
class LevelScolashipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'series', 'cycle')
    search_fields = ('name', 'series__name', 'cycle__name')
    list_filter = ('id', 'cycle', 'series')
    ordering = ('id',)
    list_per_page = per_page

@admin.register(SubjectGroup)
class SubjectGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name')
    ordering = ('id',)
    list_per_page = per_page

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name')
    ordering = ('id',)
    list_per_page = per_page

@admin.register(SanctionOrAppreciationType)
class SanctionOrAppreciationTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name')
    ordering = ('id',)
    list_per_page = per_page



@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name')
    ordering = ('id',)
    list_per_page = per_page



@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'school_cycle', 'address', 'city', 'email', 'phone', 'created_at',)
    search_fields = ('name', 'address','school_cycle', 'city', 'email', 'phone')
    list_filter = ('code', 'name','school_cycle', 'address', 'city',)
    ordering = ('id',)
    readonly_fields=('code', 'created_at', 'updated_at')
    fieldsets = (
        ('Identifiants', {'fields': ('code', 'name','school_cycle')}),
        ('Adresse', {'fields': ('address', 'city', 'postal_code', 'email', 'phone', 'website')}),
        ('Logo', {'fields': ('logo',)}),
        ('Description', {'fields': ('description',)}),
    )
    list_per_page = per_page



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'lastname', 'firstname', 'gender', 'phone','email', 'address',)
    search_fields = ('username','school', 'lastname', 'firstname', 'phone', 'email',)
    list_filter = ('username','school', 'lastname', 'firstname', 'gender', 'phone', 'email', 'address')
    ordering = ('id',)
    fieldsets = (
        ('Information Compte Utilisateur', {'fields': ('roles', 'username', 'email', 'password',)}),
        ('Profil', {'fields': ('is_admin', 'is_active', 'photo',)}),
        ('Information Général', {
            'fields': ('school', 'matricule', 'lastname', 'firstname','nickname', 'gender', 'nationality', 'birthplace', 'date_of_birth',)}),
        ('Coordonnée Personnel', {
            'fields': ('phone', 'address',)}),
        ('Information Enseignant ou Parent', {
            'fields': ('is_principal', 'is_assistant', 'hire_date', 'phone_work', 'profession')}),
        ('Réseaux sociaux', {
            'fields': ('skype', 'gmail', 'discord', 'facebook', 'linkedin','instagram', 'twitter', 'whatsapp')}),
        ('Création et modification', {'fields': ('created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2', 'role', )}),
    )
    list_per_page = per_page
    readonly_fields=('created_at', 'updated_at', 'matricule', 'id')
    
    def save_model(self, request, obj, form, change):
        if not change:
            # This is a new user; hash the password
            obj.set_password(form.cleaned_data['password'])
        else:
            # For existing users, ensure to only hash if password was changed
            if form.cleaned_data['password']:
                obj.set_password(form.cleaned_data['password'])
        
        super().save_model(request, obj, form, change)




@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ("user", "school", "school_year", "classroom", "is_paid", "is_active", "status", "created_at")
    list_filter = ("school", "school_year", "classroom", "is_paid", "is_active", "is_graduated", "is_transferred", "is_suspended")
    search_fields = ("user__full_name", "school__name", "classroom__name", "school_year__year")
    ordering = ("-created_at",)
    autocomplete_fields = ("user", "school", "children")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informations générales", {
            "fields": ("user", "school", "school_year", "classroom")
        }),
        ("Statut de l'élève", {
            "fields": ("is_paid", "is_active", "is_graduated", "is_transferred", "is_suspended", "is_withdrawn", "is_reinscribed"),
            "classes": ("collapse",),  # Permet de replier cette section
        }),
        ("Enfants (pour les parents)", {
            "fields": ("children",),
            "classes": ("collapse",),
        }),
        ("Informations système", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    def status(self, obj):
        """Affiche un statut coloré pour voir rapidement l'état de l'inscription."""
        if obj.is_withdrawn:
            color = "gray"
            text = "Retiré"
        elif obj.is_transferred:
            color = "orange"
            text = "Transféré"
        elif obj.is_suspended:
            color = "red"
            text = "Suspendu"
        elif obj.is_graduated:
            color = "green"
            text = "Admis"
        elif obj.is_paid:
            color = "blue"
            text = "Payé"
        else:
            color = "black"
            text = "En cours"
        return format_html(f'<span style="color: {color}; font-weight: bold;">{text}</span>')

    status.short_description = "Statut"

