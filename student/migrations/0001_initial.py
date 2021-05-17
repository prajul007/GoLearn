# Generated by Django 3.1.7 on 2021-05-17 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_desc', models.TextField(default=' ')),
                ('choice1', models.CharField(default='A', max_length=100)),
                ('choice2', models.CharField(default='A', max_length=100)),
                ('choice3', models.CharField(blank=True, default='A', max_length=100, null=True)),
                ('choice4', models.CharField(blank=True, default='A', max_length=100, null=True)),
                ('answer', models.CharField(default='NAN', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=30)),
                ('phone', models.CharField(default='', max_length=12)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('desc', models.TextField(default=' ')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('totalmarks', models.PositiveIntegerField(default=0)),
                ('marksscored', models.PositiveIntegerField(default=0)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('perquestime', models.PositiveIntegerField(default=60)),
                ('text', models.TextField(default=' ')),
                ('questions', models.ManyToManyField(blank=True, null=True, to='student.Questions')),
                ('topic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.topic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='savedQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.questions')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]
