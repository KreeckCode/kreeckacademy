from django.db import models
from accounts.models import User
from django.utils import timezone

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    error_code = models.CharField(max_length=100)
    error_message = models.TextField()
    status = models.CharField(max_length=20, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    last_updated_by = models.ForeignKey(User, related_name='updated_tickets', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.error_code}"

class SupportTicket(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"SupportTicket #{self.ticket.id} - {self.ticket.error_code}"