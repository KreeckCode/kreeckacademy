from django.urls import path, include
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import (
    profile, profile_single, admin_panel, 
    profile_update, change_password, 
    LecturerListView, StudentListView, 
    staff_add_view, edit_staff, 
    delete_staff, student_add_view, 
    edit_student, delete_student, ParentAdd, validate_username, register, logout_view
)
from .forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('auth/logout/', logout_view, name='logout'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('profile/', profile, name='profile'),
    path('profile/<int:id>/detail/', profile_single, name='profile_single'),
    path('setting/', profile_update, name='edit_profile'),
    path('change_password/', change_password, name='change_password'),

    path('lecturers/', LecturerListView.as_view(), name='lecturer_list'),
    path('lecturer/add/', staff_add_view, name='add_lecturer'),
    path('staff/<int:pk>/edit/', edit_staff, name='staff_edit'),
    path('lecturers/<int:pk>/delete/', delete_staff, name='lecturer_delete'),

    path('students/', StudentListView.as_view(), name='student_list'),
    path('enrol', student_add_view, name='add_student'),
    path('student/<int:pk>/edit/', edit_student, name='student_edit'),
    path('students/<int:pk>/delete/', delete_student, name='student_delete'),

    path('parents/add/', ParentAdd.as_view(), name='add_parent'),

    path('ajax/validate-username/', validate_username, name='validate_username'),

    path('register/', register, name='register'),

    # Password reset views
    path('password-reset/', PasswordResetView.as_view(
        form_class=EmailValidationOnForgotPassword,
        template_name='registration/password_reset.html'
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]