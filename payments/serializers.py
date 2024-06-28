from rest_framework import serializers

class CreateSubscriptionSerializer(serializers.Serializer):
    payment_method_id = serializers.CharField(max_length=255)
    course_id = serializers.IntegerField()
