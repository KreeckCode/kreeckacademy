from django import forms
from django.contrib.auth.models import User
from .models import *

class HackerthonForm(forms.ModelForm):
    class Meta:
        model = Hackerthon
        fields = ['title', 'description', 'tools', 'deadline', 'registration_deadline', 'price_description', 'location', 'price', 'sponsor', 'max_participants']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Retrieve all available tools from the database
        available_tools = Tool.objects.all()
        # Pass the actual objects of the tools as choices to the CheckboxSelectMultiple widget
        self.fields['tools'].widget = forms.CheckboxSelectMultiple(choices=[(tool.id, tool.name) for tool in available_tools])

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'phone', 'country', 'email', 'about', 'role']

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'file']


class ParticipantAcceptanceForm(forms.Form):
    ACCEPT_CHOICES = [(1, 'Accept'), (0, 'Reject')]
    accept = forms.ChoiceField(choices=ACCEPT_CHOICES, widget=forms.RadioSelect)

class ParticipantListForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all())
