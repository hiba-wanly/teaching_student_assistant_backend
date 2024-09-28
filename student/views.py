from django.shortcuts import render
from rest_framework.response import Response
from .serializer import StudentSignupSerializer,StudentSubjectInfoSerializer, StudentInfoSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
from .models import Student, StudentSubject,StudentSubjectInfo, StudentInfo
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from subject.models import Subject 
from general_information.models import GeneralInformation
from departments.models import Departments
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from users.permissions import IsLecturerUser,IsStudentUser
from .models import StudentSubject
from subject.serializer import SubjectSerializer
# Create your views here.
class StudentLoginView(ObtainAuthToken):
    def post( self, request , *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request} )
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        student = Student.objects.get(user=user) 
        token, create=Token.objects.get_or_create(user=user)
        response_data = {
            "user_id": user.id,
            "student_id": student.id,
            "username": user.username,
            "email": user.email,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "father_name": student.father_name,
            "department_id": student.departments.id if student.departments else None,
        }
        return Response({
            "user" : response_data,
            "token": token.key,
            "message":"login successfully"
        },status=status.HTTP_200_OK)
    

    
class StudentRegisterView(generics.GenericAPIView):
    serializer_class=StudentSignupSerializer
    def post( self, request , *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        student = Student.objects.get(user=user) 
        StudentInfo.objects.create(student = student)
        response_data = {
            "user_id": user.id,
            "student_id": student.id,
            "username": user.username,
            "email": user.email,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "father_name": student.father_name,
            "department_id": student.departments.id if student.departments else None,
        }
        return Response({
            "user" : response_data,
            "token": Token.objects.get(user=user).key,
            "message":"account created successfully"
        },status=status.HTTP_200_OK)
    
    
    
class AddStudentSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsStudentUser]   
    serialzer_class=UserSerializer
    
    def post(self, request ,format=None):
        user = request.user
        try:
            student = user.student
            student_id = student.id
            exam_number = request.data.get('exam_number')
            status1 = request.data.get('status')
            # year = request.data.get('year')
            # semester = request.data.get('semester')
            academic_year = request.data.get('academic_year')
            subject_id = request.data.get('subject_id')
            # student_id = request.data.get('student_id')
            info_gen = GeneralInformation.objects.get()
            year=info_gen.year
            semester=info_gen.semester
            
            try:
                subject = Subject.objects.get(id = subject_id)
                student = Student.objects.get(id = student_id)
                if not status1 or not year or not semester or not academic_year or not subject_id or not student_id:
                    return Response({
                    'message' : 'missing files',
                    'data' : {}
                },status=status.HTTP_400_BAD_REQUEST) 
                try:
                    get_old = StudentSubject.objects.get(
                    student =student,
                    subject = subject
                    )   
                    if get_old:
                          return Response({
                        'message' : 'you are already in this subject',
                        'data' : {}
                    },status=status.HTTP_400_BAD_REQUEST) 
                except StudentSubject.DoesNotExist:
      
                    data = StudentSubjectInfo.objects.create(
                        student= student,
                        subject = subject,
                        status = status1,
                        year = year,
                        semester = semester,
                        academic_year = academic_year
                    )
                    data2 = StudentSubject.objects.create(
                        student =student,
                        subject = subject
                    )
                    if exam_number:
                        data.exam_number =exam_number
                        data.save()
                    serialzer =   StudentSubjectInfoSerializer(data).data  
                    return Response({
                        'message' : 'student subject was added successfully',
                        'data' : serialzer
                    },status=status.HTTP_200_OK) 
            except Subject.DoesNotExist:
                 return Response({
                     'message' : 'subject not be found',
                     'data' : {}
                 },status=status.HTTP_404_NOT_FOUND)    
            except Student.DoesNotExist:
                 return Response({
                     'message' : 'student not be found',
                     'data' : {}
                 },status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
                 return Response({
                     "error": "Student not found."
                 },status=status.HTTP_404_NOT_FOUND)         
            

class StudentInfoList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsStudentUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        user = request.user
        try:
            student = user.student
            student_id = student.id
            try:
                student = StudentInfo.objects.get(student = student_id)
                serializer = StudentInfoSerializer(student)
                return Response({
                    'message' : 'Student Information get successfully',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)
            except StudentInfo.DoesNotExist:
                return Response({
                        'message' : 'can not find student information',
                        'data' : {}
                    },status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist:
                 return Response({
                     "error": "Student not found."
                 },status=status.HTTP_404_NOT_FOUND) 
                 
                 
    def post(self, request):
        user = request.user
        try:
            student = user.student
            student_id = student.id
            print("here")
            exam_number = request.data.get('exam_number')
            academic_year = request.data.get('academic_year')
            print(exam_number)
            print(academic_year)
            try:
                student_info = StudentInfo.objects.get(student = student_id)
                if exam_number:
                    student_info.exam_number = exam_number
                if academic_year:
                    student_info.academic_year = academic_year
                student_info.save()        
                serializer = StudentInfoSerializer(student_info)
                return Response({
                    'message' : 'Student Information updated successfully',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)
            except StudentInfo.DoesNotExist:
                return Response({
                        'message' : 'can not find student information',
                        'data' : {}
                    },status=status.HTTP_404_NOT_FOUND)   
        except Student.DoesNotExist:
                 return Response({
                     "error": "Student not found."
                 },status=status.HTTP_404_NOT_FOUND)          





        

class LogoutView(APIView):
    def post(self, request , format=None):
        request.auth.delete()
        response_data = {
            "user_id": "",
            "lecturer_id": "",
            "username": "",
            "email": "",
            "name": "",
        }
        return Response({
            "user" : response_data,
            "token": "",
            "message":"account logout successfully"
        },status=status.HTTP_200_OK)


class MySubjectView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsStudentUser]   
    serialzer_class=UserSerializer
    
    def get(self, request):
        user = request.user
        try:
            student = user.student
            student_id = student.id
            subject_student_ids = StudentSubject.objects.filter(student  = student_id)
            subject = Subject.objects.filter(id__in = subject_student_ids.values_list('subject_id',flat=True) )
            serializer = SubjectSerializer(subject, many=True)
            return Response({
                    'message' : 'subject get successfully',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)
        except Student.DoesNotExist:
                 return Response({
                     "error": "Student not found."
                 },status=status.HTTP_404_NOT_FOUND)     
            

class DeleteStudentSubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsStudentUser]   
    serialzer_class=UserSerializer
    
    def delete(self, request , pk):  
        user = request.user
        try:
             student = user.student
             student_id = student.id
             subject = Subject.objects.get(id = pk)
             student = Student.objects.get(id = student_id)
             subject_student = StudentSubject.objects.get(subject  = subject, student=student)
             subject_student.delete()
             subject_student_ids = StudentSubject.objects.filter(student  = student_id)
             subject = Subject.objects.filter(id__in = subject_student_ids.values_list('subject_id',flat=True) )
             serializer = SubjectSerializer(subject, many=True)
             return Response({
                 'message' : 'subject was deleted successfully',
                 'data' : serializer.data
             },status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
             return Response({
                 'message' : 'subject not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)



    











