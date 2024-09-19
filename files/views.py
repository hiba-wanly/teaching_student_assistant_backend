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
from users.permissions import IsLecturerUser,IsStudentUser

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
                'message' : 'Files was get successfully',
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
            return Response({
                'message' : 'Files was edited successfully',
                'data' : FilesSerializer(files).data
            },status=status.HTTP_200_OK)
        except Files.DoesNotExist:
            return Response({
                'message' : 'Files not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        return Response({
                'message' : 'can not delete Files',
                'data' : {}
            },status=status.HTTP_200_OK)
        
    
        
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