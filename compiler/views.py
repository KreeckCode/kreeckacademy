from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json
from django.conf import settings
from queue import Queue
import logging
from accounts.models import*
from compiler.forms import UserCodeForm
from course.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


@login_required
def get_practical_assessment(request, assessment_id):
    assessment = get_object_or_404(PracticalAssessment, id=assessment_id)
    context = {
        'assessment': assessment,
    }
    return render(request, 'compiler/practical_assessment.html', context)


def diagnostic_view(request):
    """
    View to print out current settings for debugging purposes.
    """
    config = {
        'DEBUG': settings.DEBUG,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
    }
    return JsonResponse(config)

def health_check(request):
    return JsonResponse({'status': 'ok'})


logger = logging.getLogger(__name__)

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"Received data: {data}")
            
            language = data.get('language')
            code = data.get('code')
            inputs = data.get('inputs', [])

            if not language or not code:
                print("Language or code missing")
                return JsonResponse({'error': 'Language and code are required.'}, status=400)

            print(f"Language: {language}, Code: {code}, Inputs: {inputs}")

            command = []
            if language == 'python':
                command = ['python', '-c', code]
            elif language == 'javascript':
                command = ['node', '-e', code]
            elif language == 'cpp':
                with open('temp.cpp', 'w') as f:
                    f.write(code)
                compile_command = ['g++', 'temp.cpp', '-o', 'temp']
                result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    return JsonResponse({'error': result.stderr}, status=400)
                command = ['./temp']

            try:
                print(f"Running command: {command}")
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout, stderr = process.communicate(input="\n".join(inputs))

                if process.returncode == 0:
                    print(f"Execution successful, output: {stdout}")
                    return JsonResponse({'output': stdout})
                else:
                    print(f"Execution error, stderr: {stderr}")
                    return JsonResponse({'error': stderr}, status=400)
            except Exception as e:
                print(f"Subprocess error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)

        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        except Exception as e:
            print(f"General error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    print("Invalid request method")
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



def execute_code(language, code):
    """
    Function to execute user code based on the specified language.
    This function runs the code in an isolated environment.
    """
    if language == 'python':
        command = ['python', '-c', code]
    elif language == 'html':
        command = ['echo', code]
    elif language == 'css':
        command = ['echo', code]
    elif language == 'javascript':
        command = ['node', '-e', code]
    elif language == 'cpp':
        # Save the C++ code to a temporary file
        with open('temp.cpp', 'w') as file:
            file.write(code)
        
        # Compile the C++ code this shouldnt be allowed anymore in the program
        compile_command = ['g++', 'temp.cpp', '-o', 'temp']
        compile_result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # If compilation is successful, execute the compiled binary
        if compile_result.returncode == 0:
            execution_command = ['./temp']
            execution_result = subprocess.run(execution_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return execution_result.stdout
        else:
            return compile_result.stderr


    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr


from datetime import datetime, timedelta

@login_required
def submit_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        assessment_id = request.POST.get('assessment_id')
        elapsed_time = request.POST.get('elapsed_time')  # New field from the front end
        user = request.user

        if assessment_id:
            assessment = PracticalAssessment.objects.get(id=assessment_id)
            if elapsed_time:
                # Convert elapsed time to timedelta object
                elapsed_time = timedelta(seconds=int(elapsed_time))
            else:
                elapsed_time = None
            
            # Create a new CodeSubmission with elapsed time
            CodeSubmission.objects.create(
                user=user,
                assessment=assessment,
                code=code,
                elapsed_time=elapsed_time,
            )
        else:
            CodeSubmission.objects.create(
                user=user,
                code=code,
            )

        # Redirect or return a response as needed
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'GET request not allowed'}, status=405)


# Add a view for displaying the compiler with practical assessment
@login_required
def compiler_with_assessment(request, assessment_id):
    assessment = get_object_or_404(PracticalAssessment, id=assessment_id)
    context = {
        'assessment': assessment,
        'form': UserCodeForm(),
    }
    return render(request, 'compiler/compiler.html', context)