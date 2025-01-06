from django.contrib import admin
from .models import Ticket, SupportTicket

admin.site.register(Ticket)
admin.site.register(SupportTicket)