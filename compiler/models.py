from django.db import models
from accounts.models import*
from course.models import *


class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    assessment = models.ForeignKey(PracticalAssessment, on_delete=models.CASCADE, null=True, blank=True)
    code = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    is_solution_visible = models.BooleanField(default=False)
    elapsed_time = models.DurationField(null=True, blank=True)  # New field to track elapsed time
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
