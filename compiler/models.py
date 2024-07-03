from django.db import models

class CodeSubmission(models.Model):
    """
    Model to store code submissions and their output.
    """
    language = models.CharField(max_length=20)
    code = models.TextField()
    output = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CodeSubmission {self.id} - {self.language}"
