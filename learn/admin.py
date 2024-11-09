from django.contrib import admin
from .models import Profile,Question
# Register your models here.

admin.site.register(Question)
admin.site.register(Profile)