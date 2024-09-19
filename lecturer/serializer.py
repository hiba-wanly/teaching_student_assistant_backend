from rest_framework import serializers
from .models import Lecturer
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from django.contrib import auth
import hashlib
from django.contrib.auth.hashers import check_password
from users.models import Users

class LecturerSignupSerializer(serializers.ModelSerializer):
    name = serializers.CharField( required=True)

    class Meta:
        model = Users
        fields = [ 'username' , 'email', 'password', 'name']
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
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        # self.validated_data.setdefault('is_superuser', False)
        user.set_password(password)
        user.is_lecturer=True
        user.save()
        Lecturer.objects.create(
            user=user,
            name=self.validated_data['name'],
        )
        return user   



# class LecturerLoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255, min_length =6)
#     password = serializers.CharField(max_length=68,write_only= True)
#     name=serializers.CharField(max_length=255, read_only=True)
#     access_token = serializers.CharField(max_length=255,read_only=True)
#     refresh_token = serializers.CharField(max_length=255,read_only=True)

#     class Meta:
#         model = Lecturer
#         fields = ['id' , 'email','password','name','access_token','refresh_token']

#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#         print(password)
#         print("done")
#         request = self.context.get('request')
#         sha_signature = hashlib.sha256(password.encode()).hexdigest()
#         print(sha_signature)
#         print("login")
#         user= authenticate(request = request,email = email,password=sha_signature)
#         print("hello")
#         print(user)
#         try:
#              print(email)
#              print(password)
#             #  sha_signature = hashlib.sha256(password.encode()).hexdigest()
#              user = Lecturer.objects.get(email = email,password =sha_signature)
#              print("email")
#              print(email)
#              print(sha_signature)
#              if not user:
#                  raise AuthenticationFailed("invalide credentials try again")
             
#             #  if not user:
#                 #  raise AuthenticationFailed("invalide credentials try again")
#              # if not user.is_verified:
#                  # raise AuthenticationFailed("Email is not verified")
#              user_token = user.tokens()
#              print(user)
             
#              return {
#                  'id' : user.id,
#                  'email' : user.email,
#                  'name' : user.name,
#                  'refresh_token' : str(user_token.get('refresh_token')),
#                  'access_token' : str(user_token.get('access_token'))
#              }    
#         except Lecturer.DoesNotExist:
#             raise AuthenticationFailed("invalide credentials 2 try again")



# class LecturerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lecturer
#         fields = ['name', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         return Lecturer.objects.create_user(**validated_data)