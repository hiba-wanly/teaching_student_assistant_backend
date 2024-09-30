from django.db import models
from subject.models import Subject
from departments.models import Departments
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin , Group , Permission
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import Users

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(Users , related_name="student", on_delete=models.PROTECT)
    first_name = models.CharField(max_length = 50,null= True , blank=True)
    last_name = models.CharField(max_length = 50,null= True , blank=True)
    father_name = models.CharField(max_length = 50,null= True , blank=True)
    departments = models.ForeignKey(Departments, on_delete = models.PROTECT,null= True , blank=True)
    # email = models.EmailField(unique = True,null= True , blank=True)
    # password = models.CharField(max_length = 250,null= True , blank=True )
    
    def __str__(self) :
        return self.user.username
    

    
class StudentInfo(models.Model):
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    academic_year = models.IntegerField(null= True , blank=True)
    exam_number = models.IntegerField(null= True , blank=True)

class StudentSubject(models.Model):
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT)     
    status = models.BooleanField(default=False)


class StudentSubjectInfo(models.Model):
    student = models.ForeignKey(Student, on_delete = models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete = models.PROTECT)  
    exam_number = models.IntegerField(null= True , blank=True)
    status = models.CharField(max_length = 50)
    year = models.CharField(max_length = 50)  
    semester = models.CharField(max_length = 50)
    academic_year = models.CharField(max_length = 50)  
      
    
    
