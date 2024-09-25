from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializer import AttendanceSerializer , AttendanceLOGSerializer
import datetime
from .models import Attendance, AttendanceLOG
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser

# Create your views here.
class AttendanceList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            attendance = Attendance.objects.filter(subject_id = request.data.get("subject"))
            serializer = AttendanceSerializer(attendance, many= True)
            return Response({
                'message' : 'Attendance was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)


class AttendanceDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk):
        try:
            attendance = Attendance.objects.get(id = pk)
            serializer = AttendanceSerializer(attendance)
            return Response({
                'message' : 'Attendance was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({
                'message' : 'Attendance not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            attendance = Attendance.objects.get(id = pk)
            date = request.data.get('date')
            type = request.data.get('type')
            day = request.data.get('day')
            percentage = request.data.get('percentage')
            if date:
                attendance.date = date
            if day:
                attendance.day = day    
            if type:
                attendance.type = type
            if percentage:
                attendance.percentage = percentage        
            attendance.save()
            return Response({
                'message' : 'Attendance was edited successfully',
                'data' : AttendanceSerializer(attendance).data
            },status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({
                'message' : 'Attendance not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request , pk):
        attendance = Attendance.objects.get(id = pk)
        attendance = Attendance.objects.filter(subject_id = attendance.subject_id)
        serializer = AttendanceSerializer(attendance, many= True)
        return Response({
                'message' : 'can not delete Attendance',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        
        
        
class AttendanceSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request, pk):
        attendance = Attendance.objects.filter(subject_id = pk)
        serializer = AttendanceSerializer(attendance, many= True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)  
        
        
class AttendanceLOGList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def post(self, request):
        items = request.data.get('items' , [])
        print(items)
        for item_data in items:
            serializer = AttendanceLOGSerializer(data=item_data)
            if serializer.is_valid():
                serializer.save()
        return Response({
                'message' : 'Attendance log was added successfully',
                'data' : {}
            },status=status.HTTP_200_OK)
        # return Response({
        #         'message' : 'missing fields',
        #         'data' : {}
        #     },status=status.HTTP_400_BAD_REQUEST)
    
    
class AttendanceLOGDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk):
        try:
            attendance_log = AttendanceLOG.objects.filter(attendance_id = pk)
            serializer = AttendanceLOGSerializer(attendance_log,many= True)
            return Response({
                'message' : 'Attendance Log was get successfully',
                'data' :  serializer.data
            },status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({
                'message' : 'Attendance not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)   