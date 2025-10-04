from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.urls import reverse
from .models import MoviePetition, PetitionVote

# Create your views here.
def index(request):
    petitions = MoviePetition.objects.filter(is_active=True).order_by('-created_at')

    if request.user.is_authenticated:
        for petition in petitions:
            petition.user_has_voted = petition.user_voted(request.user)
    
    template_data = {
        'petitions' : petitions,
    }
    return render(request, 'petitions/index.html', template_data)

@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if title and description:
            petition = MoviePetition.objects.create(
                title=title,
                description=description,
                created_by=request.user
            )
            messages.success(request, 'Your petition has been created successfully.')
            return redirect('petitions.index')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'petitions/create.html')

@login_required
def vote(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id, is_active=True)

    if petition.user_voted(request.user):
        messages.warning(request, 'You have already voted for this petition.')
    else:
        PetitionVote.objects.create(
            petition=petition,
            user=request.user
        )
        messages.success(request, f'You voted for "{petition.title}"!')

    return redirect('petitions.index')

def detail(request, petition_id):
    petition = get_object_or_404(MoviePetition, id=petition_id, is_active=True)
    votes = petition.votes.all().order_by('-voted_at')

    user_has_voted = False
    if request.user.is_authenticated:
        user_has_voted = petition.user_voted(request.user)

    template_data = {
        'petition' : petition,
        'votes': votes,
        'user_has_voted': user_has_voted,
    }

    return render(request, 'petitions/detail.html', template_data)