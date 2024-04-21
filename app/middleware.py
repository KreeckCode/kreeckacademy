from django.shortcuts import redirect
from django.urls import reverse

class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # If the user is authenticated, redirect to the dashboard
            if request.path == reverse('landing_page'):
                return redirect('home')
        else:
            # If the user is not authenticated, redirect to the landing page
            if request.path == reverse('home'):
                return redirect('login')

        return response
