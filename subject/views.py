from django.shortcuts import render
from rest_framework.response import Response
from .serializer import SubjectSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
from .models import Subject 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from subject.models import Subject 
from lecturer.models import SubjectLecturer, Lecturer
from general_information.models import GeneralInformation
from departments.models import Departments
from rest_framework import generics ,permissions
from users.serializer import UserSerializer
from users.permissions import IsLecturerUser,IsStudentUser

# Create your views here.
class SubjectStudentList(APIView):
    def get(self, request):
        # year = request.data.get('year')
        # semester = request.data.get('semester')
        academic_year = request.data.get('academic_year')
        info_gen = GeneralInformation.objects.get()
        subject = Subject.objects.filter(year=info_gen.year,semester=info_gen.semester,academic_year=academic_year)
        serializer = SubjectSerializer(subject, many=True)
        return Response({
                'message' : 'subject get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)


class SubjectList(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request ,format=None):
        user = request.user
        try:
            lecturer = user.lecturer
            lecturer_id = lecturer.id
            subject_lecturer_ids = SubjectLecturer.objects.filter(lecturer  = lecturer_id)
            print(subject_lecturer_ids)
            subject = Subject.objects.filter(id__in = subject_lecturer_ids.values_list('subject_id',flat=True) )
            serializer = SubjectSerializer(subject, many=True)
            return Response({
                    'message' : 'subject get successfully',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)
        except Lecturer.DoesNotExist:
            return Response({"error": "Lecturer not found."}, status=status.HTTP_404_NOT_FOUND)    

    def post(self, request,format=None):
        user = request.user
        try:
            lecturer = user.lecturer
            lecturer_id = lecturer.id
            user = Lecturer.objects.get(id = lecturer_id)
            print(lecturer_id)
            subject_name = request.data.get('subject_name')
            academic_year = request.data.get('academic_year')
            departments  = request.data.get('departments')
            tests_mark  = request.data.get('tests_mark')
            attendance_mark = request.data.get('attendance_mark')
            interviews_mark = request.data.get('interviews_mark')
            homework_mark  = request.data.get('homework_mark')
            labs_mark  = request.data.get('labs_mark')
            serializer = SubjectSerializer(data=request.data)
            info_gen = GeneralInformation.objects.get()
            year=info_gen.year
            semester=info_gen.semester
            if subject_name and academic_year and departments and semester and year:
                try : 
                    departments = Departments.objects.get(id = departments)
                    subject = Subject.objects.create(
                        subject_name = subject_name,
                        academic_year = academic_year,
                        departments = departments,
                        semester = semester,
                        year = year
                    )
                    subject_lecturer = SubjectLecturer.objects.create(
                        lecturer = user,
                        subject = subject
                    )
                    if tests_mark:
                        subject.tests_mark = tests_mark
                    if attendance_mark:
                        subject.attendance_mark = attendance_mark
                    if interviews_mark:
                        subject.interviews_mark = interviews_mark
                    if homework_mark:
                        subject.homework_mark = homework_mark  
                    if labs_mark:
                        subject.labs_mark = labs_mark 
                    subject.save()
                    ## i want to change it to return subject to lecturer
                    subject_lecturer_ids = SubjectLecturer.objects.filter(lecturer  = lecturer_id)
                    print(subject_lecturer_ids)
                    subject = Subject.objects.filter(id__in = subject_lecturer_ids.values_list('subject_id',flat=True) )
                    serializer = SubjectSerializer(subject, many=True)
                    ####
                    return Response({
                        'message' : 'subject was added successfully',
                        'data' : serializer.data
                    },status=status.HTTP_200_OK)
                except Departments.DoesNotExist:
                     return Response({
                         'message' : 'Departments not be found',
                         'data' : {}
                     },status=status.HTTP_404_NOT_FOUND)  
            return Response({
                    'message' : 'missing fields',
                    'data' : {}
                },status=status.HTTP_400_BAD_REQUEST)
        except Lecturer.DoesNotExist:
            return Response({"error": "Lecturer not found."}, status=status.HTTP_404_NOT_FOUND) 
        

class SubjectDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request , pk): 
        try:
            subject = Subject.objects.get(id = pk)
            return Response({
                'message' : 'subject was get successfully',
                'data' : SubjectSerializer(subject).data
            },status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response({
                'message' : 'subject not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        user = request.user
        try:
            lecturer = user.lecturer
            lecturer_id = lecturer.id
            subject = Subject.objects.get(id = pk)
            subject_name = request.data.get('subject_name')
            academic_year = request.data.get('academic_year')
            departments  = request.data.get('departments')
            semester  = request.data.get('semester')
            year = request.data.get('year')
            
            tests_mark  = request.data.get('tests_mark')
            attendance_mark = request.data.get('attendance_mark')
            interviews_mark = request.data.get('interviews_mark')
            homework_mark  = request.data.get('homework_mark')
            labs_mark  = request.data.get('labs_mark')
         
            if subject_name:
                subject.subject_name = subject_name
            if academic_year:
                subject.academic_year = academic_year
            if departments:
                try : 
                    departments = Departments.objects.get(id = departments)
                    subject.departments = departments
                except Departments.DoesNotExist:
                 return Response({
                     'message' : 'Departments not be found',
                     'data' : {}
                 },status=status.HTTP_404_NOT_FOUND)      
            if semester:
                subject.semester = semester  
            if year:
                subject.year = year
            if tests_mark:
                subject.tests_mark = tests_mark
            if attendance_mark:
                subject.attendance_mark = attendance_mark
            if interviews_mark:
                subject.interviews_mark = interviews_mark
            if homework_mark:
                subject.homework_mark = homework_mark  
            if labs_mark:
                subject.labs_mark = labs_mark
            
            subject.save()
            # serializer = SubjectSerializer(subject).data
            ## i want to change it to return subject to lecturer
            subject_lecturer_ids = SubjectLecturer.objects.filter(lecturer  = lecturer_id)
            print(subject_lecturer_ids)
            subject = Subject.objects.filter(id__in = subject_lecturer_ids.values_list('subject_id',flat=True) )
            serializer = SubjectSerializer(subject, many=True)
            ####
            return Response({
                'message' : ' subject was updated successfully ',
                'data' : serializer.data
            },status=status.HTTP_200_OK)

        except Subject.DoesNotExist:
            return Response({
                'message' : 'subject not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)    
    
    def delete(self, request , pk):  
        user = request.user
        try:
             lecturer = user.lecturer
             lecturer_id = lecturer.id
             subject = Subject.objects.get(id = pk)
             subject.delete()
             ## i want to change it to return subject to lecturer
             subject_lecturer_ids = SubjectLecturer.objects.filter(lecturer  = lecturer_id)
             print(subject_lecturer_ids)
             subject = Subject.objects.filter(id__in = subject_lecturer_ids.values_list('subject_id',flat=True) )
             serializer = SubjectSerializer(subject, many=True)
             ####
             return Response({
                 'message' : 'subject was deleted successfully',
                 'data' : serializer.data
             },status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
             return Response({
                 'message' : 'subject not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)



class AddLecturerToSubject(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
     
    def post(self, request):
        subject_id = request.data.get('subject')
        lecturer_id = request.data.get('lecturer')
        try:
            lecturer = Lecturer.objects.get(id = lecturer_id)
            subject = Subject.objects.get(id = subject_id)
            # Check if the lecturer is already assigned to the subject
            if SubjectLecturer.objects.filter(lecturer=lecturer, subject=subject).exists():
                return Response({
                    'message': 'Lecturer is already assigned to this subject',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            subject_lecturer = SubjectLecturer.objects.create(
                lecturer = lecturer,
                subject = subject
            )
            remaining_subject_lecturers = SubjectLecturer.objects.filter(
                subject = subject
            )
            # print(subject_lecturer)
            arr = []
            for sl in remaining_subject_lecturers:
                lect = Lecturer.objects.get(id = sl.lecturer_id)
                json = {
                    "id":lect.id,
                    "name":lect.name
                }
                arr.append(json)
            return Response({
                 'message' : 'lecturer was added to subject successfully',
                 'data' : arr
             },status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
             return Response({
                 'message' : 'subject not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)    
        except Lecturer.DoesNotExist:
             return Response({
                 'message' : 'lecturer not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)
        except SubjectLecturer.DoesNotExist:
             return Response({
                 'message': 'Lecturer is not assigned to this subject',
                 'data': {}
             }, status=status.HTTP_404_NOT_FOUND)      

    

class DeleteLecturerFromSubject(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
       
    def delete(self, request, subject ,lecturer):
        subject_id = subject
        lecturer_id = lecturer  
        try:
            lecturer = Lecturer.objects.get(id = lecturer_id)
            subject = Subject.objects.get(id = subject_id)
            subject_lecturer = SubjectLecturer.objects.get(
                lecturer = lecturer,
                subject = subject
            )
            subject_lecturer.delete()
            remaining_subject_lecturers = SubjectLecturer.objects.filter(
                subject = subject
            )
            # print(subject_lecturer)
            arr = []
            for sl in remaining_subject_lecturers:
                lect = Lecturer.objects.get(id = sl.lecturer_id)
                json = {
                    "id":lect.id,
                    "name":lect.name
                }
                arr.append(json)
            return Response({
                 'message' : 'lecturer was deleted from subject successfully',
                 'data' : arr
             },status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
             return Response({
                 'message' : 'subject not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)    
        except Lecturer.DoesNotExist:
             return Response({
                 'message' : 'lecturer not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)   
        except SubjectLecturer.DoesNotExist:
             return Response({
                 'message': 'Lecturer is not assigned to this subject',
                 'data': {}
             }, status=status.HTTP_404_NOT_FOUND)        


class GetLecturerFromSubject(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated&IsLecturerUser]   
    serialzer_class=UserSerializer
    
    def get(self, request, pk):
        subject_id = pk
        try:
            subject = Subject.objects.get(id = subject_id)
            subject_lecturer = SubjectLecturer.objects.filter(
                subject = subject
            )
            print(subject_lecturer)
            arr = []
            for sl in subject_lecturer:
                lect = Lecturer.objects.get(id = sl.lecturer_id)
                json = {
                    "id":lect.id,
                    "name":lect.name
                }
                arr.append(json)
            return Response({
                 'message' : 'lecturer was get from subject successfully',
                 'data' : arr
             },status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
             return Response({
                 'message' : 'subject not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)    
      


