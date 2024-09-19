from rest_framework import serializers
from .models import Student, StudentSubjectInfo, StudentInfo
from users.models import Users
from departments.models import Departments

class StudentSignupSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField( required=True)
    last_name = serializers.CharField( required=True)
    father_name = serializers.CharField( required=True)
    departments = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all())
    
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'father_name', 'departments']
        extra_kwargs={
            'password':{'write_only':True}
        } 
        
    def validate_email(self, value):
        if Users.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value    
    
    def save(self, **kwargs):
        user=Users(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password=self.validated_data['password']
        user.set_password(password)
        user.is_student=True
        user.save()
        Student.objects.create(
            user=user,
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            father_name=self.validated_data['father_name'],
            departments=self.validated_data['departments'], 
        )
        return user       

class StudentSubjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSubjectInfo
        fields = '__all__'   

class StudentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = '__all__'              