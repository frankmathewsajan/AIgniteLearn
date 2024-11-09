import json

from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string

from learn.models import Profile


def login(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            user_login(request, user)
            print(user)
            return redirect('index')
        else:
            return render(request, "learn/auth/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "learn/auth/login.html") if request.user.is_anonymous else redirect('index')


def generate_unique_username(user_name, existing_usernames):
    # Convert user_name to lowercase and replace spaces with underscores
    username = user_name.lower().replace(" ", "_")

    # Check if the username is unique
    while username in existing_usernames:
        # Append a random 4-digit number to the username
        username = f"{username}_{get_random_string(4, '0123456789')}"

    return username
def register(request):
    if request.method == "POST":
        user_name = request.POST["user_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        user_name = request.POST["user_name"]
        existing_usernames = set(User.objects.values_list("username", flat=True))  # Fetch existing usernames
        unique_username = generate_unique_username(user_name, existing_usernames)

        if password != confirmation:
            return render(request, "learn/auth/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email=email, password=password, username=unique_username)
            profile = Profile(user=user, first_name=user_name)
            user.save()
            profile.save()
        except IntegrityError as e:
            print(e)
            return render(request, "learn/auth/register.html", {
                "message": "Username already taken."
            })
        user_login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "learn/auth/register.html") if request.user.is_anonymous else redirect('index')


def logout(request):
    user_logout(request)
    return redirect('index')
