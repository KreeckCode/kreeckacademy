from django.contrib import admin
from .models import UserCode, UserProgress

@admin.register(UserCode)
class UserCodeAdmin(admin.ModelAdmin):
    """Admin interface for managing UserCode"""
    list_display = ('user', 'lesson', 'submitted')
    search_fields = ('user__username', 'lesson__title')

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    """Admin interface for managing UserProgress"""
    list_display = ('user', 'course', 'lesson', 'completed')
    search_fields = ('user__username', 'course__title', 'lesson__title')
