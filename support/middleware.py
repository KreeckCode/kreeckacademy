import logging
from django.shortcuts import render
from .models import SupportTicket, Ticket

logger = logging.getLogger(__name__)

def automatic_ticket_creation(error_code, error_message, user=None):
    logger.info(f"Entering automatic_ticket_creation with error_code: {error_code} and error_message: {error_message}")
    
    existing_tickets = Ticket.objects.filter(error_code=error_code, status='open')
    if existing_tickets.exists():
        logger.info(f"Existing ticket found for error_code: {error_code}")
    else:
        logger.info(f"No existing ticket found for error_code: {error_code}. Creating new ticket.")
        ticket = Ticket.objects.create(
            error_code=error_code,
            error_message=error_message
        )
        logger.info(f"Ticket created with ID: {ticket.id}")
        SupportTicket.objects.create(ticket=ticket)
        logger.info(f"SupportTicket created with ID: {ticket.id}")

class ErrorLoggingMiddleware:
    """"""
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("ErrorLoggingMiddleware initialized")

    def __call__(self, request):
        logger.info("ErrorLoggingMiddleware __call__ method invoked")
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"process_exception triggered with exception: {exception}")
        automatic_ticket_creation('AUTOMATIC_ERROR_CODE', str(exception), None)
        logger.info("Error processed and ticket creation attempted.")
        return render(request, 'common/500.html', status=500)
