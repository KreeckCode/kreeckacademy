from rest_framework import generics
from accounts.models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from SMS.settings import DEBUG

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    #set a trigger to allow all users to connect to the database if its running on a local server
    if DEBUG == False:
        permission_classes = [IsAuthenticated]
    else:
        authentication_classes = []  # No authentication classes
        permission_classes = [AllowAny]  # Allow any user (no permissions required)
    
