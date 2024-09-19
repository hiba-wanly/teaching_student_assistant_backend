from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import ActivitySerializer
import datetime
from .models import Activity
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser

# Create your views here.
class ActivityList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        activity = Activity.objects.all()
        serializer = ActivitySerializer(activity, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Activity was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)

class ActivityDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk):
        try:
            activity = Activity.objects.get(id = pk)
            serializer = ActivitySerializer(activity)
            return Response({
                'message' : 'Activity was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            return Response({
                'message' : 'Activity not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            activity = Activity.objects.get(id = pk)
            activity_full_mark = request.data.get('activity_full_mark')
            percentage = request.data.get('percentage')
            if activity_full_mark:
                activity.activity_full_mark = activity_full_mark
            if percentage:
                activity.percentage = percentage        
            activity.save()
            return Response({
                'message' : 'activity was edited successfully',
                'data' : ActivitySerializer(activity).data
            },status=status.HTTP_200_OK)
        except Activity.DoesNotExist:
            return Response({
                'message' : 'Activity not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        return Response({
                'message' : 'can not delete Activity',
                'data' : {}
            },status=status.HTTP_200_OK)
        
    
class ActivitySubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
     
    def get(self, request, pk):
        activity = Activity.objects.filter(subject_id = pk)
        serializer = ActivitySerializer(activity, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)  