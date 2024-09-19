from django.urls import path
from . import views

urlpatterns = [
    path('',views.InterviewList.as_view()),
    path('<int:pk>',views.InterviewDetail.as_view()),
    path('subject/<int:pk>',views.InterviewSubjectList.as_view()),
]