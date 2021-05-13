from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Questions)
admin.site.register(Test)
admin.site.register(Topic)
admin.site.register(savedQuestion)

