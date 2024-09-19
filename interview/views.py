from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import InterviewSerializer
import datetime
from .models import Interview
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser

# Create your views here.
class InterviewList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        interview = Interview.objects.all()
        serializer = InterviewSerializer(interview, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = InterviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Interview was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)


class InterviewDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk):
        try:
            interview = Interview.objects.get(id = pk)
            serializer = InterviewSerializer(interview)
            return Response({
                'message' : 'Interview was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Interview.DoesNotExist:
            return Response({
                'message' : 'Interview not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            interview = Interview.objects.get(id = pk)
            interview_full_mark = request.data.get('interview_full_mark')
            number_of_interview = request.data.get('number_of_interview')
            percentage = request.data.get('percentage')
            if interview_full_mark:
                interview.interview_full_mark = interview_full_mark
            if number_of_interview:
                interview.number_of_interview = number_of_interview
            if percentage:
                interview.percentage = percentage        
            interview.save()
            return Response({
                'message' : 'interview was edited successfully',
                'data' : InterviewSerializer(interview).data
            },status=status.HTTP_200_OK)
        except Interview.DoesNotExist:
            return Response({
                'message' : 'interview not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        return Response({
                'message' : 'can not delete interview',
                'data' : {}
            },status=status.HTTP_200_OK)
        
        # try:
        #     category = Category.objects.get(id = pk)
        #     category.delete()
        #     return Response({
        #         'message' : 'category was deleted successfully',
        #         'data' : {}
        #     },status=status.HTTP_200_OK)
        # except Category.DoesNotExist:
        #     return Response({
        #         'message' : 'category not be found',
        #         'data' : {}
        #     },status=status.HTTP_404_NOT_FOUND)
        
class InterviewSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request, pk):
        interview = Interview.objects.filter(subject_id = pk)
        serializer = InterviewSerializer(interview, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)  