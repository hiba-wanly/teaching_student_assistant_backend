from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from subject.models import Subject
from rest_framework_simplejwt.tokens import RefreshToken
from departments.models import Departments
from users.models import Users

# Create your models here.
class Lecturer(models.Model):
    user = models.OneToOneField(Users , related_name="lecturer", on_delete=models.CASCADE)
    name = models.CharField(unique=True, max_length = 50,null= True , blank=True)
    # email = models.EmailField(unique = True,null= True , blank=True)
    # password = models.CharField(max_length = 250 ,null= True , blank=True)
    salt = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.user.username
  
    
    

class SubjectLecturer(models.Model):
    lecturer = models.ForeignKey(Lecturer, on_delete = models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE)   