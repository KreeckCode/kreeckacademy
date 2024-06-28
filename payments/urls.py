from django.urls import path
from .views import CreateSubscriptionView, StripeWebhookView

urlpatterns = [
    path('create-subscription/', CreateSubscriptionView.as_view(), name='create-subscription'),
    path('webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
