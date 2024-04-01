from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

def execute_code(language, code):
    if language == 'python':
        command = ['python', '-c', code]
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
        data = request.POST
        language = data.get('language')
        code = data.get('code')

        try:
            # Execute code based on the selected language
            if language == 'python':
                # Execute Python code using Brython
                execute_code(language, code)
            else:
                # Handle other languages or display an error
                pass
            
            return JsonResponse({'output': 'Code executed successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'})