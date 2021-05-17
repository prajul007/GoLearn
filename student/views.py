from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import *
from rest_framework.filters import SearchFilter,OrderingFilter
from .models import *
from django.db import IntegrityError
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist


class CreateUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def create(self, request):
        try:
            user = User.objects.create_user(username=request.data['phone'], password=request.data['password'], email = request.data['email'])
        except IntegrityError:
            return Response({"USER_EXISTS": "User already exists with this phone number"}, status=400)
        request.data['user'] = user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

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
        test = Test.objects.create(topic=topic,user_is__user=request.user,text=request.data['text'],perquestion=request.data['perquestion'])

        ## Call Tesseract API for image

        ## Call Rapid API

        ## Append Question on test obj

        return Response({"id":test.id},status=200)


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

