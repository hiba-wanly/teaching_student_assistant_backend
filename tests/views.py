from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import TestsSerializer
import datetime
from .models import Tests
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser

# Create your views here.
class TestsList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        tests = Tests.objects.all()
        serializer = TestsSerializer(tests, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TestsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Tests was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)

class TestsDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk):
        try:
            tests = Tests.objects.get(id = pk)
            serializer = TestsSerializer(tests)
            return Response({
                'message' : 'Tests was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Tests.DoesNotExist:
            return Response({
                'message' : 'Tests not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            tests = Tests.objects.get(id = pk)
            test_full_mark = request.data.get('test_full_mark')
            number_of_test = request.data.get('number_of_test')
            percentage = request.data.get('percentage')
            if test_full_mark:
                tests.test_full_mark = test_full_mark
            if number_of_test:
                tests.number_of_work = number_of_test
            if percentage:
                tests.percentage = percentage        
            tests.save()
            return Response({
                'message' : 'Tests was edited successfully',
                'data' : TestsSerializer(tests).data
            },status=status.HTTP_200_OK)
        except Tests.DoesNotExist:
            return Response({
                'message' : 'Tests not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        return Response({
                'message' : 'can not delete Tests',
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
        
class TestsSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request, pk):
        tests = Tests.objects.filter(subject_id = pk)
        serializer = TestsSerializer(tests, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)  