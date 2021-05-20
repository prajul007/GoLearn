from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import *
from rest_framework import generics
import json
from rest_framework.filters import SearchFilter,OrderingFilter
from .models import *
from django.db import IntegrityError
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist


import requests
import json


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserProfileSerializer

    def create(self,request,*args,**kwargs):
        try:
            user = User.objects.create_user(username=request.data['phone'],password=request.data['password'],email=request.data['email'])
        except IntegrityError:
            return Response({"USER_EXISTS":"User already exists with this phone number"},status=400)
        request.data['user'] = user.id
        serializer = CreateUserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=200)

class UserProfile(RetrieveUpdateAPIView):

    queryset = Student.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request,*args,**kwargs):

        user = self.queryset.get(user=request.user)
        serializer = self.get_serializer(user)
        return Response(serializer.data,status=200)


    def partial_update(self, request,*args,**kwargs):

        user = self.queryset.get(user=request.user)
        serializer = self.get_serializer(user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=200)

class PastTest(ListAPIView):
    queryset = Test.objects.all().order_by('-id')
    serializer_class = PastTestListSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):

        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

class PastTestdetail(RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = PastTestSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

class SaveQuestion(ListCreateAPIView):
    queryset = savedQuestion.objects.all().order_by('-id')
    serializer_class = SavedQuestionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user__user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def create(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

class StartTest(APIView):
    permission_classes = [permissions.IsAuthenticated, ]
    def post(self, request):
        topic=Topic.objects.create(name=request.data['name'],desc=request.data['desc'])
        test = Test.objects.create(topic=topic,user=request.user,text=request.data['text'],perquestime =request.data['perquestion'])

        url = "https://question-generator.p.rapidapi.com/"

        querystring = {"text":request.data['text'],"nbr":"10"}

        headers = {
            'x-rapidapi-key': "38f45be352msh9c4b087a7f500d2p1db096jsn045d2b9d0d4a",
            'x-rapidapi-host': "question-generator.p.rapidapi.com"
            }


        response = requests.request("GET", url, headers=headers, params=querystring)
        print(response.text)
        quest = response.text.split('Question')
        
        for q in quest:
            try:
                s = q.split('Answer')
                print(s[0][7:], s[1][6:])
                qye  = Questions.objects.create(question_desc=s[0][7:], answer=s[1][6:])
                qye.save()
                test.questions.add(qye)
                print()
            except Exception:
                print()
        l = []
        ques = test.questions.all()
        for i in ques:
            d = {}
            d["questionText"] = i.question_desc
            d["contestId"] = test.id
            d["id"] = i.id
            m = []
            m.append(i.choice1)
            m.append(i.choice2)
            m.append(i.choice3)
            m.append(i.choice4)
            d["options"] = m
            d['answer'] = i.answer
            l.append(d)
        return Response(l, status=200)


class GetTest(RetrieveUpdateAPIView):
    queryset = Test.objects.all()
    serializer_class = PastTestSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(id=kwargs['id'])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=200)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(id=kwargs["id"])
        except ObjectDoesNotExist:
            return Response({"error": "Does not exist"}, status=404)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

def preprocess():
    res = '''
    Question 1:
    The aims to protect London's wildlife and wild spaces, and it manages over 40 nature reserves in Greater London.
    Answer:
    trust
    Question 2:
    The trust's oldest include Sydenham Hill Wood (pictured), which was managed by Southwark Wildlife Group before 1982 and was thus already a trust reserve at that date.
    Answer:
    reserves
    Question 3:
    The to save Gunnersbury Triangle began that same year, succeeding in 1983 when a public inquiry ruled that the site could not be developed because of its value for nature.
    Answer:
    campaign
    Question 4:
    The campaign to save Gunnersbury Triangle began that same year, succeeding in 1983 when a public ruled that the site could not be developed because of its value for nature.
    Answer:
    inquiry
    Question 5:
    The has some 50 members of staff and 500 volunteers who work together on activities such as water management, chalk grassland restoration, helping people with special needs, and giving children an opportunity to go pond-dipping.
    Answer:
    trust
    Question 6:
    The trust has some 50 members of staff and 500 volunteers who work together on activities such as water management, chalk grassland restoration, helping people with special needs, and giving an opportunity to go pond-dipping.
    Answer:
    children
    Question 7:
    The trust has some 50 members of staff and 500 volunteers who work together on activities such as water management, chalk grassland restoration, helping people with special needs, and giving children an opportunity to go pond-.
    Answer:
    dipping
    Question 8:
    The trust aims to protect London's wildlife and wild , and it manages over 40 nature reserves in Greater London.
    Answer:
    spaces
    Question 9:
    The trust aims to protect London's wildlife and wild spaces, and it manages over 40 nature in Greater London.
    Answer:
    reserves
    Question 10:
    The trust has some 50 of staff and 500 volunteers who work together on activities such as water management, chalk grassland restoration, helping

    '''

    quest = res.split('Question')
    
    for q in quest:
        try:
            s = q.split('Answer')
            print(s[0][7:], s[1][6:])
            qye  = Questions.objects.create(question_desc=s[0][7:], answer=s[1][6:])
            qye.save()
            print()
        except Exception:
            print()
