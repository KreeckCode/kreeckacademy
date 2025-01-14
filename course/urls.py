from django.urls import path
from .views import *

urlpatterns = [
    # Program urls
    path('', program_view, name='programs'),
    path('<int:pk>/detail/', program_detail, name='program_detail'),
    path('add/', program_add, name='add_program'),
    path('<int:pk>/edit/', program_edit, name='edit_program'),
    path('<int:pk>/delete/', program_delete, name='program_delete'),

    # Course urls
    path('course/<slug>/detail/', course_single, name='course_detail'),
    path('<int:pk>/course/add/', course_add, name='course_add'),
    path('course/<slug>/edit/', course_edit, name='edit_course'),
    path('course/delete/<slug>/', course_delete, name='delete_course'),

    # CourseAllocation urls
    path('course/assign/', CourseAllocationFormView.as_view(), name='course_allocation'),
    path('course/allocated/', course_allocation_view, name='course_allocation_view'),
    path('allocated_course/<int:pk>/edit/', edit_allocated_course, name='edit_allocated_course'),
    path('course/<int:pk>/deallocate/', deallocate_course, name='course_deallocate'),

    # File uploads urls
    path('course/<slug>/documentations/upload/', handle_file_upload, name='upload_file_view'),
    path('course/<slug>/documentations/<int:file_id>/edit/', handle_file_edit, name='upload_file_edit'),
    path('course/<slug>/documentations/<int:file_id>/delete/', handle_file_delete, name='upload_file_delete'),

    # Lesson urls
    path('course/<slug>/video/upload/', handle_video_upload, name='upload_video'),
    path('course/<slug>/video/<video_slug>/detail/', handle_video_single, name='video_single'),
    path('course/<slug>/video/<uuid:video_id>/edit/', handle_video_edit, name='upload_video_edit'),
    path('course/<slug>/video/<uuid:video_id>/delete/', handle_video_delete, name='upload_video_delete'),

    # Module creation
    path('course/<slug:course_slug>/create_module/', create_module, name='create_module'),
    path('<slug:course_slug>/module/<uuid:module_id>/update/', update_module, name='update_module'),
    path('<slug:course_slug>/module/<uuid:module_id>/delete/', delete_module, name='delete_module'),

    

    # Course registration
    path('course/registration/', course_registration, name='course_registration'),
    path('course/drop/', course_drop, name='course_drop'),
    
    path('my_courses/', user_course_list, name="user_course_list"),

    # Compiler view
    path('compiler/', compiler, name='compiler'),
    path('compiler/<int:lesson_id>/', compiler, name='compiler_with_lesson'),
    path('projects/create/', create_project, name='create_project'),
    path('projects/get_code/', get_project_code, name='get_project_code'),
    path('delete_project/', delete_project, name='delete_project'),
]
