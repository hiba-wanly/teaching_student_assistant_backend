from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeworkList.as_view()),
    path('<int:pk>',views.HomeworkDetail.as_view()),
    path('subject/<int:pk>',views.HomeworkSubjectList.as_view()),
]