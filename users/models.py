from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver

# Create your models here.
class Users(AbstractUser):
    is_lecturer = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    # is_superuser = models.BooleanField(default=False, null=True)
    email = models.EmailField(unique=True)  
    
    def __str__(self):
        return self.username
    
   
@receiver(post_save , sender=settings.AUTH_USER_MODEL)    
def create_auth_token(sender , instance=None , created=False ,  **kwargs):
    if created:
        Token.objects.create(user=instance)
        
         
    