from django.urls import path
from .views import *

urlpatterns = [
    path('run_code/', run_code, name='run_code'),
    path('health/', health_check, name='health_check'),
    path('diagnostic/', diagnostic_view, name='diagnostic'),
]