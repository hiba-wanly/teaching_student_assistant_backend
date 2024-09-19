from django.urls import path
from . import views

urlpatterns = [
    path('',views.AttendanceList.as_view()),
    path('<int:pk>',views.AttendanceDetail.as_view()),
    path('subject/<int:pk>',views.AttendanceSubjectList.as_view()),
    path('log',views.AttendanceLOGList.as_view()),
]