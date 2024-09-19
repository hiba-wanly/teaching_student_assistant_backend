from django.urls import path
from . import views

urlpatterns = [
    path('',views.DepartmentsList.as_view()),
    path('<int:pk>',views.DepartmentsDetail.as_view()),]