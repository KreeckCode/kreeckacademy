from common.authentication import APIKeyAuthentication
from rest_framework import generics
from course.models import Program, Course, CourseAllocation
from .serializers import ProgramSerializer, CourseSerializer, CourseAllocationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from SMS.settings import DEBUG
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class ProgramList(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    
    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny]


class ProgramDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer

    authentication_classes = [APIKeyAuthentication]
    permission_classes = [AllowAny]
    

class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    if DEBUG == False:
        authentication_classes = [APIKeyAuthentication]
        permission_classes = [AllowAny]
    else:
        authentication_classes = [] 
        permission_classes = [AllowAny] 
    

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    if DEBUG == False:
        authentication_classes = [APIKeyAuthentication]
        permission_classes = [AllowAny]
    else:
        authentication_classes = [] 
        permission_classes = [AllowAny]
    

class CourseAllocationList(generics.ListCreateAPIView):
    queryset = CourseAllocation.objects.all()
    serializer_class = CourseAllocationSerializer
    if DEBUG == False:
        authentication_classes = [APIKeyAuthentication]
        permission_classes = [AllowAny]
    else:
        authentication_classes = []
        permission_classes = [AllowAny] 
    

class CourseAllocationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CourseAllocation.objects.all()
    serializer_class = CourseAllocationSerializer
    if DEBUG == False:
        authentication_classes = [APIKeyAuthentication]
        permission_classes = [AllowAny]
    else:
        authentication_classes = []
        permission_classes = [AllowAny]
    
