
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import numpy as np  # Import NumPy

def execute_code(language, code):
    if language == 'python':
        try:
            exec(code)  # Execute the Python code
            return 'Python code executed successfully'
        except Exception as e:
            return str(e)  # Return any errors encountered during execution
    elif language == 'html':
        command = ['echo', code]
    elif language == 'css':
        command = ['echo', code]
    elif language == 'javascript':
        command = ['node', '-e', code]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        return result.stderr
    
@csrf_exempt
def run_code_view(request):
    if request.method == 'POST':
        data = request.POST  # Use request.POST to get form data
        language = data.get('language')
        code = data.get('code')
        user_input = data.get('input')  # Get user input from the input box

        try:
            # Check if the code requires input
            if 'input()' in code:
                # If it requires input, prompt the user
                if user_input is None:
                    return JsonResponse({'error': 'Input required but not provided'})

            # Execute the code
            execute_code(language, code)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'})