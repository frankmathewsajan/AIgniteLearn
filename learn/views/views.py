import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from learn.forms import ProfileForm
from learn.models import Profile, CodingQuestion


def compiler(request):
    # Retrieve all IDs of objects in CodingQuestion
    question_ids = list(CodingQuestion.objects.values_list('id', flat=True))

    # Render the template and pass the IDs as context
    return render(request, 'learn/compiler/compiler.html', {
        'ids': question_ids
    })


def get_coding_question(request, question_id):
    try:
        question = CodingQuestion.objects.get(id=question_id)
        data = {
            'title': question.title,
            'description': question.description,
            'difficulty': question.difficulty,
            'constraints': question.constraints,
            'example_input': question.example_input,
            'example_output': question.example_output
        }
        return JsonResponse(data, safe=False)
    except CodingQuestion.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)


def index(request):
    if request.user.is_authenticated:
        return render(request, "learn/index.html")
    else:
        return render(request, "learn/welcome.html")


def features(request):
    return render(request, "learn/features.html")


def leaderboard(request):
    return render(request, "learn/leaderboard.html")


def perks(request):
    return render(request, "learn/perks.html")


def hackathon(request):
    return render(request, "learn/hackathon.html")


def game(request):
    return render(request, "learn/game.html")


def about(request):
    return render(request, "learn/about.html")


def contact(request):
    return render(request, "learn/contact.html")


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
        "style_list": ["Visual", "Auditory", "Reading/Writing"],

        "interests": [
            "Biomedical Engineering",
            "Robotics and Automation",
            "Medical Imaging Technology",
            "Nanotechnology in Medicine",
            "Artificial Intelligence in Healthcare",
            "Prosthetics and Wearable Devices",
            "Healthcare Systems Optimization",
        ],
        "goals": [
            "Advance Medical Robotics and Devices",
            "Develop Analytical and Problem-Solving Skills in Engineering",
            "Enhance Research Methodologies in Biomedical Fields",
            "Innovate AI Applications for Diagnostics and Treatment",
            "Master the Design of Healthcare Systems",
            "Pioneer Sustainable Engineering Solutions for Medical Needs",
            "Contribute to Life-Saving Technologies"
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
