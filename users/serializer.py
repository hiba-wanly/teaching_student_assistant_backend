from rest_framework import serializers
from .models import Users
from lecturer.models import Lecturer
from student.models import Student


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username' , 'email' ]
    
             
             