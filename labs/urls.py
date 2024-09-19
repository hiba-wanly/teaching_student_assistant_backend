from django.urls import path
from . import views

urlpatterns = [
    path('',views.LabsList.as_view()),
    path('<int:pk>',views.LabsDetail.as_view()),
    path('subject/<int:pk>',views.LabsSubjectList.as_view()),
]