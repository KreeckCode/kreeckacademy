from django import forms
from course.models import UserCode

class UserCodeForm(forms.ModelForm):
    """
    Form to handle user code submissions, notes, and submission status.
    """
    class Meta:
        model = UserCode
        fields = ['code_main', 'code_test', 'notes', 'submitted']
