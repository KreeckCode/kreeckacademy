from django.urls import path
from . import views

urlpatterns = [
    path('', views.hackathon_list, name='hackerthon_list'),
    path('hackathon/<int:pk>/', views.hackathon_detail, name='hackerthon_detail'),
    path('hackathon/create/', views.hackathon_create, name='hackerthon_create'),
    path('hackathon/<int:pk>/update/', views.hackathon_update, name='hackerthon_update'),
    path('hackathon/<int:pk>/delete/', views.hackathon_delete, name='hackerthon_delete'),
]
