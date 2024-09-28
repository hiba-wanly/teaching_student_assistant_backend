from django.urls import path
from . import views

urlpatterns = [
    # path('',views.StudentList.as_view()),
    path('addsubjectstudent',views.AddStudentSubjectList.as_view()),
    path('studentinfo/',views.StudentInfoList.as_view()),
    path('login',views.StudentLoginView.as_view()),
    path('register',views.StudentRegisterView.as_view()),
    path('logout',views.LogoutView.as_view()),
    path('mysubject',views.MySubjectView.as_view()),
    path('deletesubjectstudent/<int:pk>',views.DeleteStudentSubjectList.as_view()),
]

