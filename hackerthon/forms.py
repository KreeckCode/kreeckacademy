from django import forms
from django.contrib.auth.models import User
from .models import *

class HackerthonForm(forms.ModelForm):
    class Meta:
        model = Hackerthon
        fields = ['title', 'description', 'tools', 'deadline', 'registration_deadline', 'price_description', 'location', 'price', 'sponsor', 'max_participants']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['first_name', 'last_name', 'phone', 'country', 'email', 'date_of_birth', 'about']

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title', 'file']

class UploadVideoForm(forms.ModelForm):
    class Meta:
        model = UploadVideo
        fields = ['title', 'video', 'summary', 'duration']

class UserRoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = ['user', 'hackerthon', 'role']

class ParticipantAcceptanceForm(forms.Form):
    ACCEPT_CHOICES = [(1, 'Accept'), (0, 'Reject')]
    accept = forms.ChoiceField(choices=ACCEPT_CHOICES, widget=forms.RadioSelect)

class ParticipantListForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all())
