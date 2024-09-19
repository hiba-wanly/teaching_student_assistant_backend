from rest_framework.response import Response
from .serializer import DepartmentsSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.forms.models import model_to_dict
from .models import Departments
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class DepartmentsList(APIView):
    
    def get(self, request):
        departments = Departments.objects.all()
        serializer = DepartmentsSerializer(departments, many=True)
        return Response({
                'message' : 'get successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = DepartmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : 'Departments was added successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        return Response({
                'message' : 'missing fields',
                'data' : {}
            },status=status.HTTP_400_BAD_REQUEST)





class DepartmentsDetail(APIView):
     
    def get(self, request , pk):
        try:
            departments = Departments.objects.get(id = pk)
            return Response({
                'message' : 'Departments was get successfully',
                'data' : DepartmentsSerializer(departments).data
            },status=status.HTTP_200_OK)
        except Departments.DoesNotExist:
            return Response({
                'message' : 'Departments not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            departments = Departments.objects.get(id = pk)
            name = request.data.get('name')
            if name:
                departments.name = name         
            departments.save()
            serializer = DepartmentsSerializer(departments)
            return Response({
                'message' : 'Departments was edited successfully',
                'data' : serializer.data
            },status=status.HTTP_200_OK)
        except Departments.DoesNotExist:
            return Response({
                'message' : 'Departments not be found',
                'data' : {}
            },status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request , pk):
         try:
             departments = Departments.objects.get(id = pk)
             departments.delete()
             return Response({
                 'message' : 'Departments was deleted successfully',
                 'data' : {}
             },status=status.HTTP_200_OK)
         except Departments.DoesNotExist:
             return Response({
                 'message' : 'Departments not be found',
                 'data' : {}
             },status=status.HTTP_404_NOT_FOUND)


    


   