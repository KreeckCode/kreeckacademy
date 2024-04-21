from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Hackerthon, Participant
from .forms import ParticipantForm, HackerthonForm

def hackerthon_list(request):
    hackerthons = Hackerthon.objects.all()
    return render(request, 'hackerthon/hackerthon_list.html', {'hackerthons': hackerthons})

def hackerthon_detail(request, pk):
    hackerthon = get_object_or_404(Hackerthon, pk=pk)
    return render(request, 'hackerthon/hackerthon_detail.html', {'hackerthon': hackerthon})

def hackerthon_create(request):
    if request.method == 'POST':
        form = HackerthonForm(request.POST)
        if form.is_valid():
            hackerthon = form.save()
            messages.success(request, 'Hackerthon created successfully!')
            return redirect('hackerthon_detail', pk=hackerthon.pk)
    else:
        form = HackerthonForm()
    return render(request, 'hackerthon/hackerthon_form.html', {'form': form})

def hackerthon_update(request, pk):
    hackerthon = get_object_or_404(Hackerthon, pk=pk)
    if request.method == 'POST':
        form = HackerthonForm(request.POST, instance=hackerthon)
        if form.is_valid():
            hackerthon = form.save()
            messages.success(request, 'Hackerthon updated successfully!')
            return redirect('hackerthon_detail', pk=hackerthon.pk)
    else:
        form = HackerthonForm(instance=hackerthon)
    return render(request, 'hackerthon/hackerthon_form.html', {'form': form})

def hackerthon_delete(request, pk):
    hackerthon = get_object_or_404(Hackerthon, pk=pk)
    if request.method == 'POST':
        hackerthon.delete()
        messages.success(request, 'Hackerthon deleted successfully!')
        return redirect('hackerthon_list')
    return render(request, 'hackerthon/hackerthon_confirm_delete.html', {'hackerthon': hackerthon})
