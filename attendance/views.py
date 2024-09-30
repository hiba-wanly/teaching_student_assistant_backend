from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from student.models import Student, StudentSubject
from subject.models import Subject
from .serializer import AttendanceSerializer , AttendanceLOGSerializer
import datetime
from .models import Attendance, AttendanceLOG
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser, IsLecturerOrStudent

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
        try:
            attendance = Attendance.objects.get(id = pk)
            attendancedata = Attendance.objects.filter(subject_id = attendance.subject_id)
            serializer = AttendanceSerializer(attendancedata, many= True)
            attendance.delete()
            return Response({
                    'message' : 'can not delete Attendance',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({
                'message' : 'Attendance can not delete',
                'data' : serializer.data
            },status=status.HTTP_404_NOT_FOUND)    
        
        
        
class AttendanceSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerOrStudent]   
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
                # try:
                    if AttendanceLOG.objects.filter(attendance =item_data.get('attendance') ,student = item_data.get('student') ).exists():
                        att_log = AttendanceLOG.objects.get(attendance =item_data.get('attendance') ,student = item_data.get('student') )
                        if item_data.get('status') == 'absent':
                            att_log.delete()
                        else :    
                            att_log.status = item_data.get('status') 
                            att_log.save()
                    else:
                        if item_data.get('status') != 'absent':
                            att = Attendance.objects.get(id =item_data.get('attendance'))
                            stu = Student.objects.get(id = item_data.get('student'))
                            data = AttendanceLOG.objects.create(
                                attendance_id = att.id,
                                student = stu,
                                status = item_data.get('status') ,
                                subject =att.subject
                            )
                        # serializer.save()
                    # if get_old:
                # except AttendanceLOG.DoesNotExist:         
                #     serializer.save()
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
        except AttendanceLOG.DoesNotExist:
            return Response({
                'message' : 'Attendance not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)   
            
            
class AttendanceLOGToStudentDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsStudentUser]   
    serialzer_class=UserSerializer  
    
    def get(self, request , pk):
        user = request.user
        try:
            student = user.student
            student_id = student.id
            data = [] 
            attendance = Attendance.objects.filter(subject_id = pk)
            for att in attendance:
                try:
                    attendance_log = AttendanceLOG.objects.get(attendance_id = att.id,student_id= student_id )
                    d = {
                        "id": att.id,
                        "date": att.date,
                        "day": att.day,
                        "type": att.type,
                        "percentage": att.percentage,
                        "subject": att.subject_id,
                        "status":attendance_log.status
                    }
                    data.append(d)
                except AttendanceLOG.DoesNotExist:
                    d = {
                        "id": att.id,
                        "date": att.date,
                        "day": att.day,
                        "type": att.type,
                        "percentage": att.percentage,
                        "subject": att.subject_id,
                        "status":""
                    }
                    data.append(d)
            # serializer = AttendanceLOGSerializer(attendance_log)
            return Response({
                'message' : 'Attendance Log was get successfully',
                'data' :  data
            },status=status.HTTP_200_OK)
        except Attendance.DoesNotExist:
            return Response({
                'message' : 'Attendance not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)          
            
           
           
class AttendanceStudentLogDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer  
    
    def get(self, request , sub, att):
        user = request.user
        try:
            subject = Subject.objects.get(id = sub)
            student = StudentSubject.objects.filter(
                subject = subject
            ) # i get id to student 
            # student.sort(key=lambda x: x['first_name'])
            # attendance_log = Attendance.objects.filter(id=att)
            arr = []
            for sl in student:
                stud = Student.objects.get(id = sl.student_id)
                if AttendanceLOG.objects.filter(student_id=sl.student_id, attendance_id = att).exists():
                    attLog = AttendanceLOG.objects.get(student_id=sl.student_id)
                    json = {
                        "student_id":stud.id,
                        "first_name":stud.first_name,
                        "last_name":stud.last_name,
                        "father_name":stud.father_name,
                        "status":attLog.status,
                        "attendance_log_id":attLog.id
                    }
                    arr.append(json)
                else :
                    json = {
                        "student_id":stud.id,
                        "first_name":stud.first_name,
                        "last_name":stud.last_name,
                        "father_name":stud.father_name,
                        "status":"",
                        "attendance_log_id":""
                    }
                    arr.append(json)
            arr.sort(key=lambda x: x['first_name'])        
            return Response({
                 'message' : 'Student was get from subject successfully',
                 'data' : arr
             },status=status.HTTP_200_OK)        
        except Subject.DoesNotExist:
             return Response({
                 'message' : 'subject not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)
        except AttendanceLOG.DoesNotExist:
             return Response({
                 'message' : 'attendanceLOG not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)            
            