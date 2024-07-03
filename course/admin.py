from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Program, Course, CourseAllocation, Upload, UploadVideo, UserCode, UserProgress, UserProject

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary')
    search_fields = ('title', 'summary')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'program', 'level', 'semester', 'credit', 'price')
    search_fields = ('title', 'code', 'summary')
    list_filter = ('program', 'level', 'semester')

class CourseAllocationAdmin(admin.ModelAdmin):
    list_display = ('lecturer', 'session')
    search_fields = ('lecturer__username', 'session__name')
    list_filter = ('lecturer', 'session')

class UploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'upload_time', 'updated_date')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

class UploadVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'timestamp', 'duration')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

class UserCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'submitted')
    search_fields = ('user__username', 'lesson__title')
    list_filter = ('user', 'lesson', 'submitted')

class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'lesson', 'completed')
    search_fields = ('user__username', 'course__title', 'lesson__title')
    list_filter = ('user', 'course', 'lesson', 'completed')

class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'language', 'created_at', 'updated_at')
    search_fields = ('user__username', 'name', 'language')
    list_filter = ('user', 'language')

admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseAllocation, CourseAllocationAdmin)
admin.site.register(Upload, UploadAdmin)
admin.site.register(UploadVideo, UploadVideoAdmin)
admin.site.register(UserCode, UserCodeAdmin)
admin.site.register(UserProgress, UserProgressAdmin)
admin.site.register(UserProject, UserProjectAdmin)

# Unregister the Group model from admin (if not used)
admin.site.unregister(Group)
