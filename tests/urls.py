from django.urls import path
from . import views

urlpatterns = [
    path('',views.TestsList.as_view()),
    path('<int:pk>',views.TestsDetail.as_view()),
    path('subject/<int:pk>',views.TestsSubjectList.as_view()),
]