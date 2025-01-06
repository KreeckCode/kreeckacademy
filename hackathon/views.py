from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Hackathon, Participant
from .forms import ParticipantForm, HackathonForm

def hackathon_list(request):
    hackathons = Hackathon.objects.all()
    return render(request, 'hackerthon/hackerthon_list.html', {'hackerthons': hackathons})

def hackathon_detail(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    return render(request, 'hackerthon/hackerthon_detail.html', {'hackerthon': hackathon})

def hackathon_create(request):
    if request.method == 'POST':
        form = HackathonForm(request.POST)
        if form.is_valid():
            hackathon = form.save()
            messages.success(request, 'Hackerthon created successfully!')
            return redirect('hackerthon_detail', pk=hackathon.pk)
    else:
        form = HackathonForm()
    return render(request, 'hackerthon/hackerthon_form.html', {'form': form})

def hackathon_update(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    if request.method == 'POST':
        form = HackathonForm(request.POST, instance=hackathon)
        if form.is_valid():
            hackathon = form.save()
            messages.success(request, 'Hackerthon updated successfully!')
            return redirect('hackerthon_detail', pk=hackathon.pk)
    else:
        form = HackathonForm(instance=hackathon)
    return render(request, 'hackerthon/hackerthon_form.html', {'form': form})

def hackathon_delete(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    if request.method == 'POST':
        hackathon.delete()
        messages.success(request, 'Hackerthon deleted successfully!')
        return redirect('hackerthon_list')
    return render(request, 'hackerthon/hackerthon_confirm_delete.html', {'hackerthon': hackathon})
