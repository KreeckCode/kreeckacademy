import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import CreateSubscriptionSerializer
from course.models import Course
from kreeckacademy.settings import *

stripe.api_key = STRIPE_LIVE_SECRET_KEY

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

            # Create a Stripe customer if not exists
            stripe_customer = stripe.Customer.list(email=user.email).data
            if not stripe_customer:
                stripe_customer = stripe.Customer.create(
                    email=user.email,
                    payment_method=payment_method_id,
                    invoice_settings={
                        'default_payment_method': payment_method_id,
                    },
                )
            else:
                stripe_customer = stripe_customer[0]

            # Attach the payment method to the customer
            stripe.PaymentMethod.attach(
                payment_method_id,
                customer=stripe_customer.id,
            )

            # Set the default payment method on the customer
            stripe.Customer.modify(
                stripe_customer.id,
                invoice_settings={
                    'default_payment_method': payment_method_id,
                },
            )

            # Create a subscription
            stripe_subscription = stripe.Subscription.create(
                customer=stripe_customer.id,
                items=[{'price': price_id}],
                expand=['latest_invoice.payment_intent'],
            )

            # Save the subscription details in the database
            Subscription.objects.create(
                user=user,
                course=course,
                stripe_subscription_id=stripe_subscription.id,
                active=True,
            )

            return Response({'status': 'subscription created'})
        return Response(serializer.errors, status=400)

class StripeWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return Response(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return Response(status=400)

        # Handle the event
        if event['type'] == 'invoice.payment_succeeded':
            # Handle successful payment
            pass
        elif event['type'] == 'invoice.payment_failed':
            # Handle failed payment
            pass

        return Response(status=200)
