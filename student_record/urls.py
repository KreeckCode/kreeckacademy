from django.urls import path
from . import views

urlpatterns = [
    # Unified records dashboard for all users
    path('dashboard/', views.records_dashboard, name='records_dashboard'),

    # Document upload using modal for students
    path('upload_document_modal/', views.upload_document_modal, name='upload_document_modal'),

    # Grade management using modal for lecturers
    path('manage_grades_modal/<int:student_id>/', views.manage_grades_modal, name='manage_grades_modal'),

    # Disciplinary action management using modal for admins
    path('manage_disciplinary_actions_modal/<int:student_id>/', views.manage_disciplinary_actions_modal, name='manage_disciplinary_actions_modal'),
]
