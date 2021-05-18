from rest_framework import serializers
from .models import *



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model= Student
        fields= "__all__"
        depth=2

class CreateUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model= Student
        fields= "__all__"

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model= Questions
        fields = "__all__"

class PastTestListSerializer(serializers.ModelSerializer):

    class Meta:
        model= Test
        fields= ['id','topic','date','totalmarks','marksscored']
        depth= 2

class PastTestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model= Test
        fields = '__all__'

class SavedQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model= savedQuestion
        fields = ["question"]
        depth= 2

