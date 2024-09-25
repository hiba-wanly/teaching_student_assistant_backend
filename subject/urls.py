from django.urls import path
from . import views

urlpatterns = [
    path('student/',views.SubjectStudentList.as_view()),
    path('',views.SubjectList.as_view()),
    path('<int:pk>',views.SubjectDetail.as_view()),
    path('addlecturertosubject',views.AddLecturerToSubject.as_view()),
    path('deleteLecturerFromSubject/<int:subject>/<int:lecturer>',views.DeleteLecturerFromSubject.as_view()),
    path('getLecturerFromSubject/<int:pk>',views.GetLecturerFromSubject.as_view()),
    path('<int:pk>',views.SubjectDetail.as_view()),
    path('getStudentFromSubject/<int:pk>',views.GetStudentsFromSubject.as_view()),
]


      