from .models import Ticket, SupportTicket

def automatic_ticket_creation(error_code, error_message, user=None):
    print(f"Entering automatic_ticket_creation with error_code: {error_code} and error_message: {error_message}")
    existing_tickets = Ticket.objects.filter(error_code=error_code, status='open')
    if not existing_tickets.exists():
        ticket = Ticket.objects.create(
            user=user,
            error_code=error_code,
            error_message=error_message
        )
        SupportTicket.objects.create(ticket=ticket, user=user)
        print(f"Ticket created with ID: {ticket.id}")
        print(f"SupportTicket created with ID: {ticket.id}")
    else:
        print(f"Existing ticket found for error_code: {error_code}")