from django.http import JsonResponse
from django.shortcuts import render

def ide(request):
    return render(request, 'ide.html')

def run_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        return JsonResponse({'code': code})  # Return the code to the frontend
    return JsonResponse({'error': 'Invalid request method.'})
