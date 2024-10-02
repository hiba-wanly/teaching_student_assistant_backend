from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import FilesSerializer
import datetime
from .models import Files
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser, IsLecturerOrStudent

# Create your views here.
class FilesList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        files = Files.objects.all()
        serializer = FilesSerializer(files, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            files = Files.objects.filter(subject_id = request.data.get("subject"))
            serializer = FilesSerializer(files, many= True)
            return Response({
                'message' : 'Files was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)

class FilesDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk):
        try:
            files = Files.objects.get(id = pk)
            serializer = FilesSerializer(files)
            return Response({
                'message' : 'File was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Files.DoesNotExist:
            return Response({
                'message' : 'Files not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            files = Files.objects.get(id = pk)
            name = request.data.get('name')
            file_path = request.FILES.get('file_path')
            published_date = request.data.get('published_date')
            available_date = request.data.get('available_date')
            type = request.data.get('type')
            if name:
                files.name = name
            if file_path:
                files.file_path = file_path
            if published_date:
                files.published_date = published_date 
            if available_date:
                files.available_date = available_date     
            if type:
                files.type = type        
            files.save()
            files2 = Files.objects.filter(subject_id = files.subject_id)
            serializer = FilesSerializer(files2, many= True)
            return Response({
                'message' : 'File was edited successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        except Files.DoesNotExist:
            return Response({
                'message' : 'Files not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        try :
            files = Files.objects.get(id = pk)
            files2 = Files.objects.filter(subject_id = files.subject_id)
            serializer = FilesSerializer(files2, many= True)
            files.delete()
            return Response({
                    'message' : 'file was delete successfully',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)
        except Files.DoesNotExist:
            return Response({
                'message' : 'Files not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)    
        
    
        
class FilesSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request, pk):
        files = Files.objects.filter(subject_id = pk)
        serializer = FilesSerializer(files, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)  