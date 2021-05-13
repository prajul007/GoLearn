from django.urls import path,include
from .views import *

urlpatterns = [
    path('myprofile/',UserProfile.as_view()),
    path('pasttest/',PastTest.as_view()),
    path('pasttest/<int:id>/',PastTestdetail.as_view()),
    path('savedques/',savedQuestion.as_view()),
]