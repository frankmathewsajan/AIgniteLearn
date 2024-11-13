import re

gcc_path = "C:/msys64/ucrt64/bin/gcc.exe"

# Function to run code for different languages

import os
import subprocess
import json
from django.http import JsonResponse
import platform


def execute_code(request):
    # Get the code and language from the request
    data = json.loads(request.body)

    language = data.get('language')
    code = data.get('code')
    user_input = data.get('user_input', '')  # User input passed in the request body

    # Temporary file setup
    temp_file = 'Main'

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

    elif language == 'c':
        file_extension = '.c'
        with open(temp_file + file_extension, 'w') as file:
            file.write(code)
        if platform.system() == 'Windows':
            command = f"gcc {temp_file + file_extension} -o {temp_file}.exe && {temp_file}.exe"
        else:
            command = f"gcc {temp_file + file_extension} -o {temp_file} && ./{temp_file}"

    elif language == 'cpp':
        file_extension = '.cpp'
        with open(temp_file + file_extension, 'w') as file:
            file.write(code)
        if platform.system() == 'Windows':
            command = f"g++ {temp_file + file_extension} -o {temp_file}.exe && {temp_file}.exe"
        else:
            command = f"g++ {temp_file + file_extension} -o {temp_file} && ./{temp_file}"

    else:
        return JsonResponse({'error': 'Unsupported language'})

    # Execute the code and capture the output
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, input=user_input, timeout=10)
        if result.returncode == 0:
            return JsonResponse({'output': result.stdout})
        else:
            return JsonResponse({'error': result.stderr})
    except subprocess.TimeoutExpired:
        return JsonResponse({'error': 'Code execution timed out'})
    except Exception as e:
        return JsonResponse({'error': str(e)})
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
