from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import LabsSerializer
import datetime
from .models import Labs
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser

# Create your views here.
class LabsList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
     
    def get(self, request):
        labs = Labs.objects.all()
        serializer = LabsSerializer(labs, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = LabsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Labs was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)


class LabsDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
     
    def get(self, request , pk):
        try:
            labs = Labs.objects.get(id = pk)
            serializer = LabsSerializer(labs)
            return Response({
                'message' : 'Labs was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Labs.DoesNotExist:
            return Response({
                'message' : 'Labs not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            labs = Labs.objects.get(id = pk)
            lab_full_mark = request.data.get('lab_full_mark')
            number_of_labs = request.data.get('number_of_labs')
            percentage = request.data.get('percentage')
            if lab_full_mark:
                labs.lab_full_mark = lab_full_mark
            if number_of_labs:
                labs.number_of_labs = number_of_labs
            if percentage:
                labs.percentage = percentage        
            labs.save()
            return Response({
                'message' : 'Labs was edited successfully',
                'data' : LabsSerializer(labs).data
            },status=status.HTTP_200_OK)
        except Labs.DoesNotExist:
            return Response({
                'message' : 'Labs not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        return Response({
                'message' : 'can not delete Labs',
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
        
class LabsSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request, pk):
        labs = Labs.objects.filter(subject_id = pk)
        serializer = LabsSerializer(labs, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)  