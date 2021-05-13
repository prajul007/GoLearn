from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

GENDER_CHOICES = (
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other"),
)


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(choices=GENDER_CHOICES, max_length=30)
    phone = models.CharField(max_length=12, default="")

class Questions(models.Model):
    question_desc = models.TextField(default=" ")
    choices = models.ManyToManyField(null=True,blank=True)
    answer = models.CharField(default='',null=True,blank=True)

class Test(models.Model):
    questions = models.ManyToManyField('Questions',null=True,blank=True)
    topic = models.ForeignKey('Topic', null=True, blank=True)
    date=models.DateField(auto_now=True)
    totalmarks = models.PositiveIntegerField(default=0)
    marksscored = models.PositiveIntegerField(default=0)
    user_id = models.OneToOneField('User')
    file = models.FileField(null=True,blank=True)
    perquestime = models.PositiveIntegerField(default=60)
    text = models.TextField(default=" ")

class Topic(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(default=" ")

class savedQuestion(models.Model):
    question = models.ForeignKey('Questions', null=True, blank=True)
    user = models.ForeignKey('User',null=True,blank=True)



