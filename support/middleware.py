import logging
from django.shortcuts import render
from .models import SupportTicket

class ErrorLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code >= 400:
            self.log_error(request, response.status_code)
        return response

    def log_error(self, request, status_code):
        error_code = f"ERROR-{status_code}"
        if not SupportTicket.objects.filter(error_code=error_code).exists():
            SupportTicket.objects.create(
                user=request.user if request.user.is_authenticated else None,
                title=f"Error {status_code}",
                description=f"An error occurred with status code {status_code} for URL {request.path}",
                error_code=error_code
            )