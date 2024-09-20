from django.contrib import admin
from backend.models.account import User, UserRole
from backend.models.admin_manager.admin_manager import LevelScolaship, SchoolCycle,SchoolSeries
from backend.models.school_manager.school_manager import School

# Register your models here.
# model from admin_manager module
@admin.register(SchoolCycle)
class SchoolCycleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name',)
    ordering = ('id',)
    
@admin.register(SchoolSeries)
class SchoolSeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name',)
    ordering = ('id',)

@admin.register(LevelScolaship)
class LevelScolashipAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'series', 'cycle')
    search_fields = ('name', 'series__name', 'cycle__name')
    list_filter = ('id', 'cycle', 'series')
    ordering = ('id',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('id', 'name')
    ordering = ('id',)

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
    
