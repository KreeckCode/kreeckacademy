from django.contrib import admin
from .models import *
from .models import Hackerthon
from .forms import HackerthonForm

class HackerthonAdmin(admin.ModelAdmin):
    form = HackerthonForm

admin.site.register(Hackerthon, HackerthonAdmin)
admin.site.register(Participant)
admin.site.register(Upload)
admin.site.register(Tool)
