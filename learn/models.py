from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Extending User Model Using a One-To-One Link
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # New fields
    first_name = models.CharField(max_length=30, blank=True)  # Add first_name field
    email = models.EmailField(blank=True)  # Optional, since user already has an email
    age = models.PositiveIntegerField(null=True, blank=True)  # Age field
    learning_style = models.CharField(max_length=50, blank=True)  # Preferred learning style
    education_level = models.CharField(max_length=50, blank=True)  # Education level
    interests = models.JSONField(default=list, blank=True)  # List of interests
    goals = models.JSONField(default=list, blank=True)  # List of goals
    is_setup = models.BooleanField(default=False)  # Profile setup status

    avatar = models.ImageField(default='profile_images/default.png', upload_to='profile_images')
    bio = models.TextField(blank=True)  # Make bio optional

    def __str__(self):
        return self.user.username
