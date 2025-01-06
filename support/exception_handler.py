from rest_framework.views import exception_handler
from .models import Ticket, SupportTicket
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Log the exception and create a support ticket
    if response is not None:
        request = context.get('request')
        error_message = str(exc)
        user = request.user if request.user.is_authenticated else None
        error_code = 'API_ERROR'
        create_ticket_if_not_exists(error_code, error_message, user)
    
    return response

def create_ticket_if_not_exists(error_code, error_message, user=None):
    existing_tickets = Ticket.objects.filter(error_code=error_code, status='open')
    if not existing_tickets.exists():
        ticket = Ticket.objects.create(
            user=user,
            error_code=error_code,
            error_message=error_message
        )
        SupportTicket.objects.create(ticket=ticket)
        logger.info(f"SupportTicket created for API error with ID: {ticket.id}")
    else:
        logger.info(f"Existing ticket found for error_code: {error_code}")
