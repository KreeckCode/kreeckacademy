from django import forms
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User

from accounts.models import User
from .models import Program, Course, CourseAllocation, Upload, UploadVideo, Lesson, PracticalAssessment

# User = settings.AUTH_USER_MODEL

class ProgramForm(forms.ModelForm):
    """Form for creating and updating Program instances."""
    class Meta:
        model = Program
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Initialise form with custom widget attributes."""
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})

class CourseAddForm(forms.ModelForm):
    """Form for creating and updating Course instances."""
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Initialise form with custom widget attributes."""
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['code'].widget.attrs.update({'class': 'form-control'})
        self.fields['credit'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['program'].widget.attrs.update({'class': 'form-control'})
        self.fields['level'].widget.attrs.update({'class': 'form-control'})
        self.fields['year'].widget.attrs.update({'class': 'form-control'})
        self.fields['semester'].widget.attrs.update({'class': 'form-control'})

class CourseAllocationForm(forms.ModelForm):
    """Form for creating and updating CourseAllocation instances."""
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by('level'),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'browser-default checkbox'}),
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ['lecturer', 'courses']

    def __init__(self, *args, **kwargs):
        """Initialise form with user-specific queryset for lecturers."""
        user = kwargs.pop('user')
        super(CourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields['lecturer'].queryset = User.objects.filter(is_lecturer=True)

class EditCourseAllocationForm(forms.ModelForm):
    """Form for editing CourseAllocation instances."""
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all().order_by('level'),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    lecturer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_lecturer=True),
        widget=forms.Select(attrs={'class': 'browser-default custom-select'}),
        label="lecturer",
    )

    class Meta:
        model = CourseAllocation
        fields = ['lecturer', 'courses']

    def __init__(self, *args, **kwargs):
        """Initialise form with user-specific queryset for lecturers."""
        super(EditCourseAllocationForm, self).__init__(*args, **kwargs)
        self.fields['lecturer'].queryset = User.objects.filter(is_lecturer=True)

class UploadFormFile(forms.ModelForm):
    """Form for uploading files to a specific course."""
    class Meta:
        model = Upload
        fields = ('title', 'file', 'course',)

    def __init__(self, *args, **kwargs):
        """Initialise form with custom widget attributes."""
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

from tinymce.widgets import TinyMCE

class UploadFormVideo(forms.ModelForm):
    """Form for uploading videos to a specific course."""
    class Meta:
        model = UploadVideo
        fields = ('title', 'video', 'course', 'summary')

    def __init__(self, *args, **kwargs):
        """Initialise form with custom widget attributes and TinyMCE for summary."""
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['video'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget = TinyMCE(attrs={'cols': 80, 'rows': 30})

class LessonForm(forms.ModelForm):
    """Form for creating and updating Lesson instances."""
    class Meta:
        model = Lesson
        fields = ('title', 'course', 'video', 'summary', 'documents')

    def __init__(self, *args, **kwargs):
        """Initialise form with custom widget attributes."""
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        self.fields['video'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['documents'].widget.attrs.update({'class': 'form-control'})

class PracticalAssessmentForm(forms.ModelForm):
    """Form for creating and updating PracticalAssessment instances."""
    class Meta:
        model = PracticalAssessment
        fields = ('title', 'lesson', 'template_code', 'solution_code', 'instructions', 'timer')

    def __init__(self, *args, **kwargs):
        """Initialise form with custom widget attributes."""
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['lesson'].widget.attrs.update({'class': 'form-control'})
        self.fields['template_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['solution_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['instructions'].widget.attrs.update({'class': 'form-control'})
        self.fields['timer'].widget.attrs.update({'class': 'form-control'})
