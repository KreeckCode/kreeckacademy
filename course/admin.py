from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

admin.site.register(Program)
admin.site.register(Course)
admin.site.register(CourseAllocation)
admin.site.register(Upload)
admin.site.register(UploadVideo)
admin.site.register(UserCode)
admin.site.register(UserProgress)
admin.site.register(UserProject)
admin.site.register(Cohort)


# Unregister the Group model from admin (if not used)
admin.site.unregister(Group)
