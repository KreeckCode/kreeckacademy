from django.urls import path
from . import views

urlpatterns = [
    path('run_code/', views.run_code, name='run_code'),
    path('submit_code/', views.submit_code, name='submit_code'),
    path('diagnostic/', views.diagnostic_view, name='diagnostic'),
    path('health/', views.health_check, name='health_check'),
    path('compiler/<int:assessment_id>/', views.compiler_with_assessment, name='compiler_with_assessment'),
    path('practical_assessment/<int:assessment_id>/', views.get_practical_assessment, name='get_practical_assessment'),
]
