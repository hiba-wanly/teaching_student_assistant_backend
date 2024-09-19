from django.shortcuts import render
from rest_framework.response import Response
from .serializer import GeneralInformationSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import make_password
from .models import GeneralInformation 
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class GeneralInformationList(APIView):
    def get(self, request):
        ginfo = GeneralInformation.objects.first()
        serializer = GeneralInformationSerializer(ginfo)
        return Response({
                'message' : 'GeneralInformation get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        semester = request.data.get('semester')
        year = request.data.get('year')
        try :
            ginfo = GeneralInformation.objects.first()
            if ginfo:
                if semester:
                    ginfo.semester = semester
                if year:
                    ginfo.year = year
                ginfo.save() 
                serializer = GeneralInformationSerializer(ginfo)
                return Response({
                    'message' : 'GeneralInformation get successfully',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)
            else:
                if not semester or not year:
                    return Response({
                        'message' : 'missing fields',
                        'data' : {}
                    },status=status.HTTP_400_BAD_REQUEST)
                ginfo = GeneralInformation.objects.create(
                    semester = semester,
                    year = year
                )
                serializer = GeneralInformationSerializer(ginfo)
                return Response({
                    'message' : 'GeneralInformation get successfully',
                    'data' : serializer.data
                },status=status.HTTP_200_OK)

        except GeneralInformation.DoesNotExist:
            # if not semester or not year:
                return Response({
                    'message' : 'missing fields',
                    'data' : {}
                },status=status.HTTP_400_BAD_REQUEST)
            # ginfo = GeneralInformation.objects.create(
            #     semester = semester,
            #     year = year
            # )
            # serializer = GeneralInformationSerializer(ginfo)
            # return Response({
            #     'message' : 'GeneralInformation get successfully',
            #     'data' : serializer.data
            # },status=status.HTTP_200_OK)







