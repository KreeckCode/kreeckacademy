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

COHORT_CHOICES = (
    ("2023A", "2023 Cohort A"),
    ("2023B", "2023 Cohort B"),
    ("2024A", "2024 Cohort A"),
    ("2024B", "2024 Cohort B"),
)

class ProgramManager(models.Manager):
    def search(self, query=None):
        """
        Searches for programs based on a query string.
        """
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(summary__icontains=query)
                         )
            qs = qs.filter(or_lookup).distinct()
        return qs

class Program(models.Model):
    """
    Model representing an academic program (e.g., Computer Science, Mathematics).
    """
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(null=True, blank=True)

    objects = ProgramManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('program_detail', kwargs={'pk': self.pk})

class CourseManager(models.Manager):
    def search(self, query=None):
        """
        Searches for courses based on a query string.
        """
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
    """
    Model representing a course within a program.
    """
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, unique=True, null=True)
    credit = models.IntegerField(null=True, default=0)
    summary = models.TextField(max_length=200, blank=True, null=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.CharField(max_length=25, choices=LEVEL, null=True)
    year = models.IntegerField(choices=YEARS, default=0)
    semester = models.CharField(choices=SEMESTER, max_length=200, null=True, blank=True)
    cohort = models.CharField(choices=COHORT_CHOICES, max_length=200, null=True, blank=True)
    is_elective = models.BooleanField(default=False, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    objects = CourseManager()

    def __str__(self):
        return "{0} ({1})".format(self.title, self.code, self.price)

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})

    @property
    def is_current_semester(self):
        """
        Property to check if the course is in the current semester.
        This assumes there is a Semester model that tracks the current semester.
        """
        from app.models import Semester
        try:
            current_semester = Semester.objects.get(is_current_semester=True)
            return self.semester == current_semester.semester
        except Semester.DoesNotExist:
            return False

    @property
    def is_current_cohort(self):
        """
        Property to check if the course is part of the current cohort.
        Useful if the school opts to use cohort-based tracking instead of semester.
        """
        from app.models import Cohort
        try:
            current_cohort = Cohort.objects.get(is_current_cohort=True)
            return self.cohort == current_cohort.cohort
        except Cohort.DoesNotExist:
            return False

# Cohort model to represent different academic cohorts
class Cohort(models.Model):
    """
    Model representing a cohort (e.g., 2023 Cohort A).
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_current_cohort = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Ensure only one cohort is marked as current at a time.
        """
        if self.is_current_cohort:
            Cohort.objects.filter(is_current_cohort=True).update(is_current_cohort=False)
        super().save(*args, **kwargs)

# Modified pre-save signal to handle the course slug creation
def course_pre_save_receiver(sender, instance, *args, **kwargs):
    """
    Pre-save signal to generate a unique slug for the course if it doesn't exist.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(course_pre_save_receiver, sender=Course)

class CourseAllocation(models.Model):
    """
    Model to represent the allocation of courses to lecturers.
    """
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='allocated_lecturer')
    courses = models.ManyToManyField(Course, related_name='allocated_course')
    session = models.ForeignKey("app.Session", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.lecturer.get_full_name

    def get_absolute_url(self):
        return reverse('edit_allocated_course', kwargs={'pk': self.pk})

class Upload(models.Model):
    """
    Model to manage course file uploads (e.g., documents, spreadsheets).
    """
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to='course_files/', validators=[FileExtensionValidator(['pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        """
        Get a short string representation of the file type.
        """
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
        """
        Delete the file from storage when deleting the model instance.
        """
        self.file.delete()
        super().delete(*args, **kwargs)

from uuid import uuid4
from django.utils.translation import gettext_lazy as _

class Module(models.Model):
    """
    Model representing a module within a course.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255)
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class UploadVideo(models.Model):
    """
    Model to manage video uploads for course modules.
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
        """
        Delete the video from storage when deleting the model instance.
        """
        self.video.delete()
        super().delete(*args, **kwargs)

class PracticalAssessment(models.Model):
    """
    Model representing a practical coding assessment for a lesson.
    """
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
    """
    Pre-save signal to generate a unique slug for practical assessments.
    """
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(practical_assessment_pre_save_receiver, sender=PracticalAssessment)

class UserCode(models.Model):
    """
    Model to track user-submitted code for a lesson.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(UploadVideo, on_delete=models.CASCADE)
    code_main = models.TextField(null=True, blank=True)
    code_test = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"

class UserProgress(models.Model):
    """
    Model to track user progress through course lessons.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(UploadVideo, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.lesson.title}"

class UserProject(models.Model):
    """
    Model to represent a user-created project.
    """
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
