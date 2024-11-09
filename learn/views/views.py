import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from learn.forms import ProfileForm
from learn.models import Profile


def index(request):
    if request.user.is_authenticated:
        return render(request, "learn/index.html")
    else:
        return redirect('login')

@login_required
def setup(request):
    if request.method == "POST":
        # Assuming the user is already authenticated
        user = request.user
        user_profile = user.profile

        # Parse the JSON data from the request body
        data = json.loads(request.body)

        # Update the user profile with the data received
        user_profile.first_name = data.get("fullName", "")
        user_profile.email = data.get("email", "")
        user_profile.age = data.get("age", "")  # Assuming you have an age field in the user_profile
        user_profile.bio = data.get("bio", "")
        user_profile.learning_style = data.get("learningStyle", "")
        user_profile.education_level = data.get("educationLevel", "")
        user_profile.interests = data.get("interests", [])
        user_profile.goals = data.get("goals", [])
        user_profile.is_setup = True

        # Save the updated user_profile
        user_profile.save()

        # Return a JSON response indicating success
        return JsonResponse({"message": "Profile updated successfully."}, status=200)

    # If not a POST request, return a method not allowed response

    return render(request, "learn/user/setup.html", {
        "profile": Profile.objects.filter(user=request.user).first(),
        "edu_list": ["Primary", "Secondary", "High School", "Undergraduate", "Graduate", "Professional"],
        "style_list": ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"],
        "interests": ["Oceanography",
                      "Satellite Technology",
                      "Earth Observation",
                      "Remote Sensing",
                      "Marine Biology",
                      "Exoplanets",
                      "Climate Science",
                      "Add Your Own"],
        "goals": [
            "Explore Planets and Satellites",
            "Develop Critical Thinking in Science",
            "Enhance Research Skills",
            "Build Satellite Expertise",
            "Master Space Concepts",
            "Develop Remote Sensing Skills",
            "Contribute to Climate Solutions"
        ]

    })

@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    initial_data = {
        'first_name': user_profile.user.first_name,
        'email': user_profile.user.email,
        'interests': ', '.join(user_profile.interests),
        'goals': ', '.join(user_profile.goals),
    }
    form = ProfileForm(instance=user_profile, initial=initial_data)

    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'learn/user/profile.html', context)
