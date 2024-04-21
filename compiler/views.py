from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

#@cache_page(60 * 60 )
def compiler(request):
    """
    this should be ona different environment because someone can easily break the software
    
    """
    return render(request, 'compiler/compiler.html')

def execute_code(language, code):
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

def run_code_view(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        code = request.POST.get('code')
        try:
            output = execute_code(language, code)
            return JsonResponse({'output': output})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid request method.'})