from django.urls import path
from .views import *

urlpatterns = [
    path('team/manage/', manage_support_team, name='manage_support_team'),
    path('create_ticket/', create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/update/', update_ticket, name='update_ticket'),
    path('ticket/<int:ticket_id>/delete/', delete_ticket, name='delete_ticket'),
    path('dashboard/', support_dashboard, name='support_dashboard'),
    path('<int:ticket_id>/', support_ticket_detail, name='support_ticket_detail'),
    path('trigger-test-error/', trigger_test_error, name='trigger_test_error'),
    path('trigger-automatic-error/', trigger_automatic_error, name='trigger_automatic_error'),
]
