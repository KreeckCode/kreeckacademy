from django.contrib import admin
from .models import *
from .models import Hackathon
from .forms import HackathonForm

class HackathonAdmin(admin.ModelAdmin):
    form = HackathonForm

admin.site.register(Hackathon, HackathonAdmin)
admin.site.register(Participant)
admin.site.register(Upload)
admin.site.register(Tool)
