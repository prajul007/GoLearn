from django.urls import path,include
from .views import *

urlpatterns = [
    path('myprofile/',UserProfile.as_view()),
    path('createuser/',CreateUser.as_view()),
    path('pasttest/',PastTest.as_view()),
    path('pasttest/<int:id>/',PastTestdetail.as_view()),
    path('savedques/',SaveQuestion.as_view()),
    path('starttest/',StartTest.as_view()),
    path('getquiz/<int:id>',GetTest.as_view()),
]

