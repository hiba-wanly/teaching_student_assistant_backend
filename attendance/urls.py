from django.urls import path
from . import views

urlpatterns = [
    path('',views.AttendanceList.as_view()),
    path('<int:pk>',views.AttendanceDetail.as_view()),
    path('subject/<int:pk>',views.AttendanceSubjectList.as_view()),
    path('log',views.AttendanceLOGList.as_view()),
    path('log/<int:pk>',views.AttendanceLOGDetail.as_view()),
    path('logtostudent/<int:pk>',views.AttendanceLOGToStudentDetail.as_view()),
    path('subject/student/<int:sub>/<int:att>',views.AttendanceStudentLogDetail.as_view()),
]