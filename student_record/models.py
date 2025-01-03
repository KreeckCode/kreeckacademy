from django.db import models
from django.conf import settings
from course.models import Course
from accounts.models import Student
from django.utils import timezone

class StudentRecord(models.Model):
    """
    Model to store student records, including enrolled courses and account details.
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_record')
    enrolled_courses = models.ManyToManyField(Course, related_name='enrolled_students', blank=True)
    account_expiry_date = models.DateField(null=True, blank=True)
    is_account_active = models.BooleanField(default=True)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.student.student.username} - Student Record"

    def add_course(self, course):
        """Add a course to the student's enrolled courses."""
        self.enrolled_courses.add(course)

    def remove_course(self, course):
        """Remove a course from the student's enrolled courses."""
        self.enrolled_courses.remove(course)
    
    def update_expiry(self, new_expiry_date):
        """Update the account expiry date."""
        self.account_expiry_date = new_expiry_date
        self.save()
    
    def check_account_status(self):
        """Check if the account is still active based on the expiry date."""
        if self.account_expiry_date and timezone.now().date() > self.account_expiry_date:
            self.is_account_active = False
            self.save()
        return self.is_account_active

    def update_outstanding_balance(self, amount):
        """Update the outstanding balance for the student."""
        self.outstanding_balance += amount
        self.save()

class PaymentRecord(models.Model):
    """
    Model to store payment records for student accounts.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='payment_records')
    payment_date = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    proof_of_payment = models.FileField(upload_to='payments/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    payment_plan = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment Record for {self.student_record.student.student.username} on {self.payment_date}"

    def approve_payment(self):
        """Approve the payment."""
        self.is_approved = True
        self.save()

class PaymentPlan(models.Model):
    """
    Model to handle payment plans for students.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='payment_plans')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Payment Plan for {self.student_record.student.student.username}"

    def deactivate_plan(self):
        """Deactivate the payment plan once completed."""
        self.is_active = False
        self.save()

class PersonalDocument(models.Model):
    """
    Model to handle important personal documents for students.
    """
    DOCUMENT_TYPES = (
        ('ID', 'Identification'),
        ('PR', 'Proof of Residency'),
        ('MR', 'Medical Record'),
        ('AC', 'Academic Record'),
    )
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='personal_documents')
    document_type = models.CharField(max_length=2, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending Verification'), ('Verified', 'Verified'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.student_record.student.student.username}"

    def verify_document(self):
        """Mark the document as verified."""
        self.status = 'Verified'
        self.save()

    def reject_document(self, reason):
        """Mark the document as rejected, with a reason."""
        self.status = 'Rejected'
        self.save()

class EnrollmentHistory(models.Model):
    """
    Model to track enrollment history of a student.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='enrollment_history')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    completion_status = models.CharField(max_length=20, choices=[('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Dropped', 'Dropped')], default='In Progress')

    def __str__(self):
        return f"Enrollment History for {self.student_record.student.student.username} in {self.course.title}"

class AttendanceRecord(models.Model):
    """
    Model to track attendance for students in courses.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"Attendance for {self.student_record.student.student.username} in {self.course.title} on {self.date}"

class Grade(models.Model):
    """
    Model to store grades for students in various courses.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.CharField(max_length=255)
    grade = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Grade for {self.student_record.student.student.username} in {self.course.title}"

class DisciplinaryAction(models.Model):
    """
    Model to handle disciplinary actions for students.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='disciplinary_actions')
    incident_date = models.DateField()
    description = models.TextField()
    action_taken = models.TextField()
    status = models.CharField(max_length=20, choices=[('Open', 'Open'), ('Resolved', 'Resolved')], default='Open')

    def __str__(self):
        return f"Disciplinary Action for {self.student_record.student.student.username} on {self.incident_date}"

class Achievement(models.Model):
    """
    Model to track student achievements.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=255)
    description = models.TextField()
    date_awarded = models.DateField()

    def __str__(self):
        return f"Achievement: {self.title} for {self.student_record.student.student.username}"

class InternshipPlacement(models.Model):
    """
    Model to handle internship placements for students.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='internships')
    company_name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    supervisor_name = models.CharField(max_length=255, null=True, blank=True)
    supervisor_contact = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Internship at {self.company_name} for {self.student_record.student.student.username}"

class Feedback(models.Model):
    """
    Model to handle course and staff feedback from students.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='feedback')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    rating = models.IntegerField()
    date_submitted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.student_record.student.student.username} for {self.course.title}"

class Notification(models.Model):
    """
    Model to track notifications sent to students.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.student_record.student.student.username} on {self.date_sent}"

class AcademicProgress(models.Model):
    """
    Model to track academic progress for students.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='academic_progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_updated = models.DateField(auto_now=True)

    def __str__(self):
        return f"Progress for {self.student_record.student.student.username} in {self.course.title}"

class EngagementMetrics(models.Model):
    """
    Model to track student engagement metrics.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='engagement_metrics')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    participation_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    last_accessed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Engagement for {self.student_record.student.student.username} in {self.course.title}"

class EventParticipation(models.Model):
    """
    Model to track event participation of students.
    """
    student_record = models.ForeignKey(StudentRecord, on_delete=models.CASCADE, related_name='event_participations')
    event_name = models.CharField(max_length=255)
    participation_date = models.DateField()
    certificate_awarded = models.BooleanField(default=False)

    def __str__(self):
        return f"Event Participation by {self.student_record.student.student.username} in {self.event_name}"
