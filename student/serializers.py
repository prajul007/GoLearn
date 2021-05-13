from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model= User
        fields= "__all__"

class PastTestListSerializer(serializers.ModelSerializer):

    class Meta:
        model= Test
        fields= ['id','topic','date','totalmarks','marksscored']
        depth= 2

class PastTestSerializer(serializers.ModelSerializer):

    class Meta:
        model= Test
        fields = '_all'
        depth= 2

class SavedQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model= savedQuestion
        fields = ["question"]
        depth= 2

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model= Questions
        fields = '_all'
        depth= 2