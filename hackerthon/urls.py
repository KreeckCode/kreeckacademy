from django.urls import path
from . import views

urlpatterns = [
    path('', views.hackerthon_list, name='hackerthon_list'),
    path('hackerthon/<int:pk>/', views.hackerthon_detail, name='hackerthon_detail'),
    path('hackerthon/create/', views.hackerthon_create, name='hackerthon_create'),
    path('hackerthon/<int:pk>/update/', views.hackerthon_update, name='hackerthon_update'),
    path('hackerthon/<int:pk>/delete/', views.hackerthon_delete, name='hackerthon_delete'),
]
