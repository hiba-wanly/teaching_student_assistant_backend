from django.urls import path
from . import views

urlpatterns = [
    path('',views.ActivityList.as_view()),
    path('<int:pk>',views.ActivityDetail.as_view()),
    path('subject/<int:pk>',views.ActivitySubjectList.as_view()),
]