from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save
from django.db.models import Q
from .utils import *
import moviepy.editor as mp

# Constants for choices
YEARS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
)

BACHELOR_DEGREE = "Bachelor"
MASTER_DEGREE = "Master"

LEVEL = (
    (BACHELOR_DEGREE, "Bachelor Degree"),
    (MASTER_DEGREE, "Master Degree"),
)

FIRST = "First"
SECOND = "Second"
THIRD = "Third"

SEMESTER = (
    (FIRST, "First"),
    (SECOND, "Second"),
    (THIRD, "Third"),
)

class ProgramManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(summary__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs

class Program(models.Model):
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(null=True, blank=True)

    objects = ProgramManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('program_detail', kwargs={'pk': self.pk})

class CourseManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(summary__icontains=query) |
                         Q(code__icontains=query) |
                         Q(slug__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs

class Course(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, unique=True, null=True)
    credit = models.IntegerField(null=True, default=0)
    summary = models.TextField(max_length=200, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    year = models.IntegerField(choices=YEARS, default=0)
    semester = models.CharField(choices=SEMESTER, max_length=200)
    is_elective = models.BooleanField(default=False, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    objects = CourseManager()

    def __str__(self):
        return "{0} ({1})".format(self.title, self.code, self.price)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    @property
    def is_current_semester(self):
        from app.models import Semester
        current_semester = Semester.objects.get(is_current_semester=True)
        return self.semester == current_semester.semester

def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(course_pre_save_receiver, sender=Course)

class CourseAllocation(models.Model):
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='allocated_lecturer')
    courses = models.ManyToManyField(Course, related_name='allocated_course')
    session = models.ForeignKey("app.Session", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.lecturer.get_full_name

    def get_absolute_url(self):
        return reverse('edit_allocated_course', kwargs={'pk': self.pk})

class Upload(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='course_files/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        ext = str(self.file).split(".")[-1]
        if ext in ['doc', 'docx']:
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext in ['xls', 'xlsx']:
            return 'excel'
        elif ext in ['ppt', 'pptx']:
            return 'powerpoint'
        elif ext in ['zip', 'rar', '7zip']:
            return 'archive'

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

from django.db import models
from uuid import uuid4
from django.utils.translation import gettext_lazy as _

class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class UploadVideo(models.Model):
    """_summary_

    Args:
        models (_type_): _description_

    Returns:
        _type_: _description_
    """
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', null=True, blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    video = models.FileField(upload_to='course_videos/', validators=[FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])])
    summary = models.TextField(null=True, blank=True)
    duration = models.DurationField(null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    documents = models.ForeignKey(Upload, on_delete=models.CASCADE, related_name='lesson_documents', null=True, blank=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('video_single', kwargs={'slug': self.course.slug, 'video_slug': self.slug})

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)




class PracticalAssessment(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    lesson = models.ForeignKey(UploadVideo, on_delete=models.CASCADE)
    template_code = models.TextField(null=True, blank=True)
    solution_code = models.TextField(null=True, blank=True)
    instructions = models.TextField(null=True, blank=True)
    timer = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('practical_assessment_detail', kwargs={'slug': self.slug})

def practical_assessment_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(practical_assessment_pre_save_receiver, sender=PracticalAssessment)

class UserCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(UploadVideo, on_delete=models.CASCADE)
    code_main = models.TextField(null=True, blank=True)
    code_test = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

class UserProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(UploadVideo, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.lesson.title}"

class UserProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=20)
    code_main = models.TextField(null=True, blank=True)
    code_test = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user.username} - {self.name}"

    class Meta:
        unique_together = ('user', 'name')