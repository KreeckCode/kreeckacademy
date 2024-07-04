from django import forms
from .models import Ticket, SupportTicket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['error_message']

class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status', 'error_message']

class AddSupportUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)