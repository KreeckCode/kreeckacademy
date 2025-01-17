# support/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from accounts.models import User
from .models import Ticket, SupportTicket
from .forms import TicketForm, AddSupportUserForm, TicketUpdateForm
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

# Check if the user is a support team member
def is_support(user):
    return user.groups.filter(name='SupportTeam').exists()

@login_required
@user_passes_test(is_support)
def manage_support_team(request):
    support_group, created = Group.objects.get_or_create(name='SupportTeam')
    if request.method == 'POST':
        form = AddSupportUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = User.objects.get(username=username)
                support_group.user_set.add(user)
                return redirect('manage_support_team')
            except User.DoesNotExist:
                form.add_error('username', 'User does not exist')
    else:
        form = AddSupportUserForm()

    support_users = support_group.user_set.all()
    context = {
        'form': form,
        'support_users': support_users
    }
    return render(request, 'support/manage_support_team.html', context)

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.error_code = 'USER_REPORTED'  # Example error code
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketForm()
    return render(request, 'tickets/create_ticket.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

@login_required
@user_passes_test(is_support)
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.last_updated_by = request.user
            ticket.last_updated_at = timezone.now()
            ticket.save()
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketUpdateForm(instance=ticket)
    return render(request, 'tickets/update_ticket.html', {'form': form, 'ticket': ticket})

@login_required
@user_passes_test(is_support)
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('support_dashboard')
    return render(request, 'tickets/confirm_delete.html', {'ticket': ticket})

def automatic_ticket_creation(error_code, error_message, user=None):
    print("Entering automatic_ticket_creation")
    logger.info("Entering automatic_ticket_creation")
    try:
        existing_tickets = Ticket.objects.filter(error_code=error_code, status='open')
        if existing_tickets.exists():
            print(f"Existing ticket found for error_code: {error_code}")
            logger.info(f"Existing ticket found for error_code: {error_code}")
        else:
            print(f"No existing ticket found for error_code: {error_code}. Creating new ticket.")
            logger.info(f"No existing ticket found for error_code: {error_code}. Creating new ticket.")
            ticket = Ticket.objects.create(
                user=user,
                error_code=error_code,
                error_message=error_message
            )
            print(f"Ticket created with ID: {ticket.id}")
            logger.info(f"Ticket created with ID: {ticket.id}")
            support_ticket = SupportTicket.objects.create(ticket=ticket)
            print(f"SupportTicket created with ID: {support_ticket.id}")
            logger.info(f"SupportTicket created with ID: {support_ticket.id}")
    except Exception as e:
        print(f"Error creating Ticket or SupportTicket: {e}")
        logger.error(f"Error creating Ticket or SupportTicket: {e}")

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("ErrorLoggingMiddleware __call__ method invoked")
        logger.info("ErrorLoggingMiddleware __call__ method invoked")
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        print(f"process_exception triggered with exception: {exception}")
        logger.error(f"process_exception triggered with exception: {exception}")
        automatic_ticket_creation('AUTOMATIC_ERROR_CODE', str(exception), request.user if request.user.is_authenticated else None)
        print("Error processed and ticket creation attempted.")
        logger.info("Error processed and ticket creation attempted.")
        return render(request, 'common/500.html', status=500)

def is_support_team(user):
    return user.groups.filter(name='SupportTeam').exists()

@login_required
@user_passes_test(is_support_team)
def support_dashboard(request):
    tickets = SupportTicket.objects.select_related('ticket').order_by('-ticket__created_at')
    return render(request, 'support/dashboard.html', {'tickets': tickets})

@login_required
@user_passes_test(is_support_team)
def support_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    if request.method == 'POST':
        form = TicketUpdateForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.last_updated_by = request.user
            ticket.last_updated_at = timezone.now()
            ticket.save()
            return redirect('support_dashboard')
    else:
        form = TicketUpdateForm(instance=ticket)
    return render(request, 'support/ticket_detail.html', {'form': form, 'ticket': ticket})

@login_required
def trigger_test_error(request):
    print("Trigger test error view invoked")
    logger.info("Trigger test error view invoked")
    try:
        raise ValueError("This is a manually triggered test error.")
    except ValueError as e:
        print(f"Manually triggered error: {e}")
        logger.error(f"Manually triggered error: {e}")
        automatic_ticket_creation('MANUAL_ERROR_CODE', str(e), request.user)
        print("Manually triggered error processed and ticket creation attempted.")
        logger.info("Manually triggered error processed and ticket creation attempted.")
        return render(request, 'common/500.html', status=500)

def trigger_automatic_error(request):
    print("Trigger automatic error view invoked")
    logger.info("Trigger automatic error view invoked")
    raise ValueError("This is an automatic test error.")
