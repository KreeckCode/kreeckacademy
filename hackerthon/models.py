from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save
from accounts.models import User
from hackerthon.utils import *
from hackerthon.choices import *


class Tool(models.Model):
    name = models.CharField(max_length=100, choices=TOOL_CHOICES)

    def __str__(self):
        return self.name

class Hackerthon(models.Model):
    slug = models.SlugField(blank=True, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    tools = models.ManyToManyField(Tool)
    deadline = models.DateTimeField()
    registration_deadline = models.DateTimeField()
    price_description = models.TextField()
    location = models.CharField(max_length=100, choices=COUNTRY_CHOICES)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    sponsor = models.CharField(max_length=50, blank=True, null=True)
    max_participants = models.PositiveIntegerField(default=10)
    accepted_participants = models.ManyToManyField(User, related_name='accepted_participants', blank=True)
    rejected_participants = models.ManyToManyField(User, related_name='rejected_participants', blank=True)

    def get_absolute_url(self):
        return reverse('hackerthon_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackerthon = models.ForeignKey(Hackerthon, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=60, blank=True, null=True)
    country = models.CharField(max_length=60, choices=COUNTRY_CHOICES)
    email = models.EmailField()
    #the user should tell us about themselves
    about = models.CharField(max_length=700)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.hackerthon.title} - {self.country}"

class UserRole(models.Model):
    ROLES = (
        ('Participant', 'Participant'),
        ('Master', 'Master'),
        ('Project Manager', 'Project Manager'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hackerthon = models.ForeignKey(Hackerthon, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.user.username} - {self.hackerthon.title} - {self.role}"

class Upload(models.Model):
    title = models.CharField(max_length=100)
    hackerthon = models.ForeignKey(Hackerthon, on_delete=models.CASCADE)
    file = models.FileField(upload_to='hackerthon_files/', validators=[FileExtensionValidator(['xd','py','css','html','ps','pdf', 'docx', 'doc', 'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7zip'])])
    updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
    upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.file)[6:]

    def get_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext)-1]

        if ext == 'doc' or ext == 'docx':
            return 'word'
        elif ext == 'pdf':
            return 'pdf'
        elif ext == 'xls' or ext == 'xlsx':
            return 'excel'
        elif ext == 'ppt' or ext == 'pptx':
            return 'powerpoint'
        elif ext == 'zip' or ext == 'rar' or ext == '7zip':
            return 'archive'

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)



class UploadVideo(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True)
    hackerthon = models.ForeignKey(Hackerthon, on_delete=models.CASCADE)
    video = models.FileField(upload_to='hackerthon_videos/', validators=[FileExtensionValidator(['mp4', 'mkv', 'wmv', '3gp', 'f4v', 'avi', 'mp3'])])
    summary = models.TextField(null=True, blank=True,)
    duration = models.DurationField(null=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('video_single', kwargs={'slug': self.hackerthon.slug, 'video_slug': self.slug})

    def delete(self, *args, **kwargs):
        self.video.delete()
        super().delete(*args, **kwargs)


def video_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(video_pre_save_receiver, sender=UploadVideo)