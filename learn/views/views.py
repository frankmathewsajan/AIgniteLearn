import base64
import io
import json
import os
import random
import re
import subprocess
import threading

import numpy as np
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from learn.forms import ProfileForm
from learn.models import Profile, Question


def engg(request):
    return render(request, "learn/engg.html")


def run_face_script(venv_python_path, face_script_path):
    """Function to execute the face.py script asynchronously."""
    try:
        process = subprocess.Popen(
            [venv_python_path, face_script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()

        print("Proctoring tool launched successfully.")
        if stdout:
            print("STDOUT:", stdout.decode())
        if stderr:
            print("STDERR:", stderr.decode())
    except Exception as e:
        print(f"Error launching proctoring tool: {e}")


def sort_log(log_data):
    # Regex to match log entries in the format "timestamp - message"
    log_entries = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (.+)", log_data)

    # Group by message
    grouped_logs = {}
    for timestamp, message in log_entries:
        if message not in grouped_logs:
            grouped_logs[message] = []
        grouped_logs[message].append(timestamp)

    # Summarize
    summary = []
    for message, timestamps in grouped_logs.items():
        start_time = timestamps[0]
        end_time = timestamps[-1]
        count = len(timestamps)
        summary.append(f"{message}\n  Count: {count}\n  Time Range: {start_time} to {end_time}")

    # Output the summary
    return "\n\n".join(summary)


def exam(request):
    print(10)
    if request.method == 'POST':
        if request.method == 'POST':
            try:
                # Parse incoming JSON data
                data = json.loads(request.body)

                # Extract values from the data
                status = data.get('status')
                time_left = data.get('timeLeft')
                answers = data.get('answers')

                # Print or log the answers for now
                print(f"Exam Status: {status}, Time Left: {time_left}")
                print(f"Answers: {answers}")

                # Example: Saving answers to the database (add your own logic here)
                # You can save the data to a model, such as ExamSubmission, with the answers
                # For simplicity, we are just printing them

                # Return a success response
                return JsonResponse({'message': 'Exam data submitted successfully'}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    # Path to the face.py script
    face_script_path = os.path.join(os.path.dirname(__file__), 'face.py')

    # Path to the virtual environment's Python interpreter
    venv_python_path = r"C:\Users\MagnumOpus\PycharmProjects\AIgniteLearn\.venv\Scripts\python.exe"

    # Launch the face.py script asynchronously
    threading.Thread(target=run_face_script, args=(venv_python_path, face_script_path)).start()

    # Retrieve all questions for the exam
    try:
        questions = Question.objects.all()
    except Exception as e:
        print(f"Error retrieving questions: {e}")
        questions = []

    return render(request, 'learn/exam.html', {'questions': questions})


def index(request):
    if request.user.is_authenticated:
        return render(request, "learn/index.html")
    else:
        return redirect('welcome')


def welcome(request):
    return render(request, "learn/welcome.html")


def report(request):
    log_file_path = r"C:\Users\MagnumOpus\PycharmProjects\AIgniteLearn\log.txt"
    with open(log_file_path, "r") as log_file:
        # Process the log file to get the summary
        summary = sort_log(log_file.read())
    return render(request, "learn/report.html", {
        "log": summary
    })


def home(request):
    return render(request, "learn/home.html")


def about(request):
    if request.user.is_authenticated:
        return render(request, "learn/about.html")


def contact(request):
    if request.user.is_authenticated:
        return render(request, "learn/contact.html")


@csrf_exempt
def analysis(request):
    return render(request, "learn/analysis.html")


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


@csrf_exempt
def process_frame(request):
    if request.method == 'POST':
        try:
            # Parse JSON payload from request.body
            body = json.loads(request.body)
            frame_data = body['frame'].split(',')[1]  # Extract Base64 data after the header

            # Decode the Base64 image
            img_data = base64.b64decode(frame_data)
            img = Image.open(io.BytesIO(img_data))  # Create PIL Image from decoded data
            img = np.array(img)  # Convert to NumPy array for ML processing

            # Run ML model (replace with your model's code)
            result = run_ml_model(img)

            # Return the result as JSON
            return JsonResponse({'result': result})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def run_ml_model(frame):
    # Placeholder for ML model processing

    return random.choice(range(100))
