from django.contrib import admin
from backend.models.account import User, UserRole
from backend.models.admin_manager.admin_manager import LevelScolaship, SchoolCycle,SchoolSeries

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
