import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Subscription
from .serializers import CreateSubscriptionSerializer
from course.models import Course
from djstripe.models import Customer, Subscription as DjstripeSubscription

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CreateSubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            payment_method_id = serializer.validated_data['payment_method_id']
            course_id = serializer.validated_data['course_id']
            user = request.user

            course = Course.objects.get(id=course_id)
            price_id = course.price_id  # Assuming you have a Stripe price ID for each course

            # Create a Stripe customer and djstripe customer object
            customer, created = Customer.get_or_create(subscriber=user)
            if created:
                customer.add_payment_method(payment_method_id)

            # Create a subscription
            stripe_subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{'price': price_id}],
                expand=['latest_invoice.payment_intent'],
            )

            # Save the subscription details in the database
            DjstripeSubscription.sync_from_stripe_data(stripe_subscription)
            Subscription.objects.create(
                user=user,
                course=course,
                stripe_subscription_id=stripe_subscription.id,
                active=True,
            )

            return Response({'status': 'subscription created'})
        return Response(serializer.errors, status=400)

from djstripe import views as djstripe_views

class StripeWebhookView(djstripe_views.ProcessWebhookView):
    pass