from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import *
from rest_framework.filters import SearchFilter,OrderingFilter
from .models import *
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist

class UserProfile(RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

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

class SaveQuestion(ListAPIView):
    queryset = savedQuestion.objects.all().order_by('-id')
    serializer_class = SavedQuestionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

