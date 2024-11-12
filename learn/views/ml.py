import json
import os
import threading

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from learn.models import Question
from .__init__ import run_face_script, sort_log


@csrf_exempt
def analysis(request):
    return render(request, "learn/ml/analysis.html")


def report(request):
    log_file_path = r"C:\Users\MagnumOpus\PycharmProjects\AIgniteLearn\log.txt"
    with open(log_file_path, "r") as log_file:
        # Process the log file to get the summary
        summary = sort_log(log_file.read())
    return render(request, "learn/ml/report.html", {
        "log": summary
    })


@csrf_exempt
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
    face_script_path = os.path.join(os.path.dirname(__file__), '../../temp/temp/face.py')

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

    return render(request, 'learn/ml/exam.html', {
        'questions': questions,
        "total_questions": len(questions)
    })
