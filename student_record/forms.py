from django import forms
from .models import StudentRecord, PaymentRecord, PersonalDocument, Grade, AttendanceRecord, DisciplinaryAction, Achievement

class StudentRecordForm(forms.ModelForm):
    class Meta:
        model = StudentRecord
        fields = ['account_expiry_date', 'is_account_active', 'enrolled_courses']

class PaymentRecordForm(forms.ModelForm):
    class Meta:
        model = PaymentRecord
        fields = ['amount', 'proof_of_payment']

class PersonalDocumentForm(forms.ModelForm):
    class Meta:
        model = PersonalDocument
        fields = ['document_type', 'document_file']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['course', 'assignment', 'grade', 'feedback']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['course', 'date', 'status']

class DisciplinaryActionForm(forms.ModelForm):
    class Meta:
        model = DisciplinaryAction
        fields = ['incident_date', 'description', 'action_taken', 'status']

class AchievementForm(forms.ModelForm):
    class Meta:
        model = Achievement
        fields = ['title', 'description', 'date_awarded']