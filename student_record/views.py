from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import StudentRecord, PaymentRecord, PersonalDocument, Grade, AttendanceRecord, DisciplinaryAction, Achievement
from .forms import StudentRecordForm, PaymentRecordForm, PersonalDocumentForm, GradeForm, AttendanceForm, DisciplinaryActionForm, AchievementForm

@login_required
def records_dashboard(request):
    """
    Unified view for students, lecturers, and admins to see their respective dashboards.
    """
    context = {
        'user': request.user,
        'show_modals': True
    }

    # If the user is a student, add student-specific data to context
    if request.user.is_student:
        student_record = get_object_or_404(StudentRecord, student__student=request.user)
        context['student_record'] = student_record
        context['upload_document_form'] = PersonalDocumentForm()

    # If the user is a lecturer, add lecturer-specific data to context
    if request.user.is_lecturer:
        student_records = StudentRecord.objects.all()
        context['student_records'] = student_records
        context['grade_form'] = GradeForm()

    # If the user is an admin, add admin-specific data to context
    if request.user.is_superuser:
        student_records = StudentRecord.objects.all()
        context['student_records'] = student_records
        context['disciplinary_form'] = DisciplinaryActionForm()

    return render(request, 'records/records_dashboard.html', context)

@login_required
def upload_document_modal(request):
    """
    Handle document upload for students using modal.
    """
    if request.method == 'POST' and request.user.is_student:
        form = PersonalDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.student_record = get_object_or_404(StudentRecord, student__student=request.user)
            document.save()
            return redirect('records_dashboard')
    return redirect('records_dashboard')

@staff_member_required
def manage_grades_modal(request, student_id):
    """
    Handle grades management for a particular student using modal.
    """
    if request.method == 'POST' and request.user.is_lecturer:
        student_record = get_object_or_404(StudentRecord, pk=student_id)
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.student_record = student_record
            grade.save()
            return redirect('records_dashboard')
    return redirect('records_dashboard')

@staff_member_required
def manage_disciplinary_actions_modal(request, student_id):
    """
    Handle disciplinary actions for a student using modal.
    """
    if request.method == 'POST' and request.user.is_superuser:
        student_record = get_object_or_404(StudentRecord, pk=student_id)
        form = DisciplinaryActionForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.student_record = student_record
            action.save()
            return redirect('records_dashboard')
    return redirect('records_dashboard')
