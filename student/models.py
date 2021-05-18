from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30)
    phone = models.CharField(max_length=12, default="")

class Questions(models.Model):
    question_desc = models.TextField(default=" ")
    choice1 = models.CharField(default="A",max_length=100)
    choice2 = models.CharField(default="A",max_length=100)
    choice3 = models.CharField(null=True, blank=True, default="A",max_length=100)
    choice4 = models.CharField(null=True, blank=True, default="A",max_length=100)
    answer = models.CharField(default='NAN',max_length=100)

class Test(models.Model):
    questions = models.ManyToManyField('Questions',null=True,blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, null=True, blank=True)
    date=models.DateField(auto_now=True)
    totalmarks = models.PositiveIntegerField(default=0)
    marksscored = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    file = models.FileField(null=True,blank=True)
    perquestime = models.PositiveIntegerField(default=60)
    text = models.TextField(default=" ")

class Topic(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(default=" ")

class savedQuestion(models.Model):
    question = models.ForeignKey('Questions',on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('Student',on_delete=models.CASCADE, null=True,blank=True)



