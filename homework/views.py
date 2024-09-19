from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import HomeworkSerializer
import datetime
from .models import Homework
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser

# Create your views here.
class HomeworkList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        homework = Homework.objects.all()
        serializer = HomeworkSerializer(homework, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = HomeworkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Homework was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)

class HomeworkDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk):
        try:
            homework = Homework.objects.get(id = pk)
            serializer = HomeworkSerializer(homework)
            return Response({
                'message' : 'Homework was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Homework.DoesNotExist:
            return Response({
                'message' : 'Homework not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            homework = Homework.objects.get(id = pk)
            homework_full_mark = request.data.get('homework_full_mark')
            number_of_work = request.data.get('number_of_work')
            percentage = request.data.get('percentage')
            file = request.FILES.get('file')
            if homework_full_mark:
                homework.homework_full_mark = homework_full_mark
            if number_of_work:
                homework.number_of_work = number_of_work
            if percentage:
                homework.percentage = percentage 
            if file:
                homework.file = file           
            homework.save()
            return Response({
                'message' : 'homework was edited successfully',
                'data' : HomeworkSerializer(homework).data
            },status=status.HTTP_200_OK)
        except Homework.DoesNotExist:
            return Response({
                'message' : 'homework not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        return Response({
                'message' : 'can not delete homework',
                'data' : {}
            },status=status.HTTP_200_OK)
        
        # try:
        #     homework = Homework.objects.get(id = pk)
        #     homework.soft_delete()
        #     return Response({
        #         'message' : 'Homework was deleted successfully',
        #         'data' : {}
        #     },status=status.HTTP_200_OK)
        # except Homework.DoesNotExist:
        #     return Response({
        #         'message' : 'Homework not be found',
        #         'data' : {}
        #     },status=status.HTTP_404_NOT_FOUND)
        
class HomeworkSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request, pk):
        homework = Homework.objects.filter(subject_id = pk)
        serializer = HomeworkSerializer(homework, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)  