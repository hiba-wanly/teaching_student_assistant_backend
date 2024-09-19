from django.urls import path
from . import views

urlpatterns = [
    path('',views.FilesList.as_view()),
    path('<int:pk>',views.FilesDetail.as_view()),
    path('subject/<int:pk>',views.FilesSubjectList.as_view()),
]