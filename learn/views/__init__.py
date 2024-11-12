import os
import re
import subprocess

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

gcc_path = "C:/msys64/ucrt64/bin/gcc.exe"
@csrf_exempt
# Function to run code for different languages
def execute_code(request):
    # Get the code and language from request
    language = request.POST.get('language')
    code = request.POST.get('code')

    # Set up a temporary file to hold the code
    temp_file = 'Main'

    # Depending on the language, write the code to a specific file type
    if language == 'python':
        file_extension = '.py'
        with open(temp_file + file_extension, 'w') as file:
            file.write(code)
        command = f"python3 {temp_file + file_extension}"

    elif language == 'java':
        file_extension = '.java'
        with open(temp_file + file_extension, 'w') as file:
            file.write(code)
        command = f"javac {temp_file + file_extension} && java {temp_file}"

    elif language == 'javascript':
        file_extension = '.js'
        with open(temp_file + file_extension, 'w') as file:
            file.write(code)
        command = f"node {temp_file + file_extension}"

    else:
        return JsonResponse({'error': 'Unsupported language'})

    # Execute the code and capture the output
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return JsonResponse({'output': result.stdout})
        else:
            return JsonResponse({'error': result.stderr})
    except subprocess.TimeoutExpired:
        return JsonResponse({'error': 'Code execution timed out'})
    finally:
        # Clean up temporary files
        if os.path.exists(temp_file + file_extension):
            os.remove(temp_file + file_extension)
        if os.path.exists(temp_file):
            os.remove(temp_file)


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
