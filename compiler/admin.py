from django.contrib import admin
from .models import CodeSubmission

@admin.register(CodeSubmission)
class CodeSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'timestamp', 'is_solution_visible', 'elapsed_time')
    search_fields = ('user__username', 'assessment__title', 'code')
    list_filter = ('is_solution_visible', 'timestamp')
