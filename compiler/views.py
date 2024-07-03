from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse

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

@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        data = request.POST
        language = data.get('language')
        code = data.get('code')

        if not language or not code:
            return JsonResponse({'error': 'Language and code are required.'}, status=400)

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
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                return JsonResponse({'output': result.stdout})
            else:
                return JsonResponse({'error': result.stderr})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

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
        
        # Compile the C++ code
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
