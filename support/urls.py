from django.urls import path
from .views import manage_support_team, create_ticket, ticket_detail, update_ticket, delete_ticket, support_dashboard, support_ticket_detail

urlpatterns = [
    path('manage_support_team/', manage_support_team, name='manage_support_team'),
    path('create_ticket/', create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', ticket_detail, name='ticket_detail'),
    path('ticket/<int:ticket_id>/update/', update_ticket, name='update_ticket'),
    path('ticket/<int:ticket_id>/delete/', delete_ticket, name='delete_ticket'),
    path('support/dashboard', support_dashboard, name='support_dashboard'),
    path('support/<int:ticket_id>/', support_ticket_detail, name='support_ticket_detail'),
]