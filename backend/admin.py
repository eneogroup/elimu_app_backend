from django.contrib import admin
from backend.models.account import *
from backend.models.admin_manager.admin_manager import LevelScolaship, SchoolCycle,SchoolSeries
from backend.models.school_manager.school_manager import School

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

@admin.register(LevelScolaship)
class LevelScolashipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'series', 'cycle')
    search_fields = ('name', 'series__name', 'cycle__name')
    list_filter = ('id', 'cycle', 'series')
    ordering = ('id',)
    list_per_page = per_page

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name')
    ordering = ('id',)
    list_per_page = per_page

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_admin', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'role__name')
    list_filter = ('id', 'username', 'email', 'role', 'is_admin', 'is_active', 'created_at',)
    ordering = ('id',)
    fieldsets = (
        ('Identifiants', {'fields': ('username', 'email', 'password')}),
        ('Profil', {'fields': ('role', 'is_admin', 'is_active')}),
        ('Création et modification', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields=('created_at', 'updated_at')
    list_per_page = per_page


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'address', 'city', 'email', 'phone', 'created_at',)
    search_fields = ('name', 'address', 'city', 'email', 'phone')
    list_filter = ('code', 'name', 'address', 'city', 'email', 'phone', 'created_at',)
    ordering = ('id',)
    readonly_fields=('code', 'created_at', 'updated_at')
    fieldsets = (
        ('Identifiants', {'fields': ('code', 'name')}),
        ('Adresse', {'fields': ('address', 'city', 'postal_code', 'email', 'phone', 'website')}),
        ('Logo', {'fields': ('logo',)}),
        ('Description', {'fields': ('description',)}),
    )
    list_per_page = per_page


@admin.register(StaffProfile)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'lastname', 'firstname', 'gender', 'phone', 'address',)
    search_fields = ('user__username', 'lastname', 'firstname', 'gender', 'phone', 'address')
    list_filter = ('user__username', 'lastname', 'firstname', 'gender', 'phone', 'address')
    ordering = ('user__id',)
    fieldsets = (
        ('Utilisateur', {'fields': ('user',)}),
        ('Personnel', {'fields': ('lastname', 'firstname', 'gender', 'nationality', 'birthplace', 'phone', 'address', 'date_of_birth', 'photo',)}),
        ('Réseaux sociaux', {'fields': ('skype', 'gmail', 'discord', 'facebook', 'linkedin','instagram', 'twitter', 'whatsapp')}),
    )
    list_per_page = per_page
    readonly_fields=('created_at', 'updated_at')


@admin.register(ParentOfStudent)
class ParentOfStudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lastname', 'firstname', 'gender', 'phone', 'address',)
    search_fields = ('user__username', 'lastname', 'firstname', 'gender', 'phone', 'address')
    list_filter = ('user__username', 'lastname', 'firstname', 'gender', 'phone', 'address')
    ordering = ('user__id',)
    fieldsets = (
        ('Utilisateur', {'fields': ('user',)}),
        ('Information Personnel', {'fields': ('lastname', 'firstname', 'gender', 'nationality', 'birthplace', 'phone', 'address', 'date_of_birth', 'photo',)}),
        ('Réseaux sociaux', {'fields': ('skype', 'gmail', 'discord', 'facebook', 'linkedin','instagram', 'twitter', 'whatsapp')}),
    )
    list_per_page = per_page
    readonly_fields=('created_at', 'updated_at')



@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ('id', 'matricule','user', 'display_parents', 'lastname', 'firstname', 'gender', 'phone', 'address',)
    search_fields = ('id', 'matricule', 'user__username', 'lastname', 'firstname', 'phone', 'address')
    list_filter = ('id', 'matricule', 'user__username', 'lastname', 'firstname', 'gender', 'phone', 'address')
    ordering = ('user__id',)
    fieldsets = (
        ('Utilisateur', {'fields': ('matricule', 'user', 'parents')}),
        ('Information Personnel', {'fields': ('lastname', 'firstname', 'gender', 'nationality', 'birthplace', 'phone', 'address', 'date_of_birth', 'photo',)}),
        ('Réseaux sociaux', {'fields': ('skype', 'gmail', 'discord', 'facebook', 'linkedin','instagram', 'twitter', 'whatsapp')}),
    )
    list_per_page = per_page
    readonly_fields=('created_at', 'updated_at')
