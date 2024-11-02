from django.contrib import admin
from .models import (
    StudentRecord, PaymentRecord, PaymentPlan, PersonalDocument,
    EnrollmentHistory, AttendanceRecord, Grade, DisciplinaryAction,
    Achievement, InternshipPlacement, Feedback
)

# Admin class to manage StudentRecord model in the Django admin site
@admin.register(StudentRecord)
class StudentRecordAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student', 'account_expiry_date', 'is_account_active', 'outstanding_balance')
    # Fields to search in the admin search bar
    search_fields = ('student__student__username', 'student__student__first_name', 'student__student__last_name')
    # Filters available in the admin list view
    list_filter = ('is_account_active',)
    # Default ordering of the list view
    ordering = ('student',)

# Admin class to manage PaymentRecord model in the Django admin site
@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'payment_date', 'amount', 'is_approved', 'payment_plan')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username',)
    # Filters available in the admin list view
    list_filter = ('is_approved', 'payment_plan')
    # Default ordering of the list view (descending by payment date)
    ordering = ('-payment_date',)

# Admin class to manage PaymentPlan model in the Django admin site
@admin.register(PaymentPlan)
class PaymentPlanAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'total_amount', 'installment_amount', 'due_date', 'is_active')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username',)
    # Filters available in the admin list view
    list_filter = ('is_active',)
    # Default ordering of the list view
    ordering = ('due_date',)

# Admin class to manage PersonalDocument model in the Django admin site
@admin.register(PersonalDocument)
class PersonalDocumentAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'document_type', 'status')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'document_type')
    # Filters available in the admin list view
    list_filter = ('status', 'document_type')
    # Default ordering of the list view
    ordering = ('student_record',)

# Admin class to manage EnrollmentHistory model in the Django admin site
@admin.register(EnrollmentHistory)
class EnrollmentHistoryAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'course', 'enrollment_date', 'completion_status')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'course__title')
    # Filters available in the admin list view
    list_filter = ('completion_status',)
    # Default ordering of the list view
    ordering = ('enrollment_date',)

# Admin class to manage AttendanceRecord model in the Django admin site
@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'course', 'date', 'status')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'course__title')
    # Filters available in the admin list view
    list_filter = ('status', 'course')
    # Default ordering of the list view
    ordering = ('date',)

# Admin class to manage Grade model in the Django admin site
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'course', 'assignment', 'grade')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'course__title', 'assignment')
    # Filters available in the admin list view
    list_filter = ('course',)
    # Default ordering of the list view
    ordering = ('course',)

# Admin class to manage DisciplinaryAction model in the Django admin site
@admin.register(DisciplinaryAction)
class DisciplinaryActionAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'incident_date', 'description', 'status')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'description')
    # Filters available in the admin list view
    list_filter = ('status',)
    # Default ordering of the list view
    ordering = ('incident_date',)

# Admin class to manage Achievement model in the Django admin site
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'title', 'date_awarded')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'title')
    # Default ordering of the list view
    ordering = ('date_awarded',)

# Admin class to manage InternshipPlacement model in the Django admin site
@admin.register(InternshipPlacement)
class InternshipPlacementAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'company_name', 'role', 'start_date', 'end_date')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'company_name', 'role')
    # Filters available in the admin list view
    list_filter = ('company_name',)
    # Default ordering of the list view
    ordering = ('start_date',)

# Admin class to manage Feedback model in the Django admin site
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('student_record', 'course', 'rating', 'date_submitted')
    # Fields to search in the admin search bar
    search_fields = ('student_record__student__student__username', 'course__title')
    # Filters available in the admin list view
    list_filter = ('rating', 'course')
    # Default ordering of the list view (descending by submission date)
    ordering = ('-date_submitted',)
