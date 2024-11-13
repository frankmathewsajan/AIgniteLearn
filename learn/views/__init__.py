import re

gcc_path = "C:/msys64/ucrt64/bin/gcc.exe"

# Function to run code for different languages

import subprocess
import os
import tempfile
import json
from django.http import JsonResponse


def execute_code(request):
    # Get the code, language, and user input from the request
    data = json.loads(request.body)
    language = data.get('language')
    code = data.get('code')
    user_input = data.get('user_input', '')

    # Define language-specific settings
    extensions = {
        'python': '.py',
        'java': '.java',
        'javascript': '.js',
        'c': '.c',
        'cpp': '.cpp'
    }
    commands = {
        'python': lambda file: f"python3 {file}",
        'java': lambda file: f"javac {file} && java {file.replace('.java', '')}",
        'javascript': lambda file: f"node {file}",
        'c': lambda file: f"gcc {file} -o {file.replace('.c', '')} && ./{file.replace('.c', '')}",
        'cpp': lambda file: f"g++ {file} -o {file.replace('.cpp', '')} && ./{file.replace('.cpp', '')}"
    }

    # Validate language
    if language not in extensions:
        return JsonResponse({'error': 'Unsupported language'})

    # Create a temporary file
    try:
        with tempfile.NamedTemporaryFile(suffix=extensions[language], delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name

        # Run the code
        command = commands[language](temp_file_path)
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, input=user_input, timeout=10
        )
        if result.returncode == 0:
            return JsonResponse({'output': result.stdout})
        else:
            return JsonResponse({'error': result.stderr})
    except subprocess.TimeoutExpired:
        return JsonResponse({'error': 'Code execution timed out'})
    except Exception as e:
        return JsonResponse({'error': f'Internal server error: {str(e)}'})
    finally:
        # Cleanup temporary files
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


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
