from django import forms
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from accounts.models import User
from .models import *

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
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control'})

class UploadFormVideo(forms.ModelForm):
    """Form for uploading videos to a specific course."""
    class Meta:
        model = UploadVideo
        fields = ('title', 'video', 'course', 'module', 'summary', 'documents')

    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['video'].widget.attrs.update({'class': 'form-control'})
        self.fields['summary'].widget = TinyMCE(attrs={'cols': 80, 'rows': 30})
        self.fields['course'].widget.attrs.update({'class': 'form-control'})
        if course:
            self.fields['module'].queryset = course.modules.all()
        self.fields['module'].required = False
        self.fields['module'].widget = forms.Select(attrs={'id': 'module-select'})
        self.fields['documents'].widget.attrs.update({'class': 'form-control'})

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title']

class CombinedUploadVideoForm(forms.Form):
    upload_video_form = UploadFormVideo()
    module_form = ModuleForm()

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


