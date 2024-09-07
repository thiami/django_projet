# public/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Activite, Ville, TypeActivite, Registration
from .forms import RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
def index(request):
    return render(request, 'index.html')

def activite_list(request):
    types_activites = TypeActivite.objects.prefetch_related('activite_set')  # Précharge les activités liées à chaque type
    context = {
        'types_activites': types_activites,
    }
    return render(request, 'activite_list.html', context)

@login_required
def register_for_activity(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)

    if request.method == 'POST':
        # Vérifier si l'utilisateur est déjà inscrit
        if Registration.objects.filter(user=request.user, activity=activite).exists():
            messages.warning(request, "Vous êtes déjà inscrit à cette activité.")
        else:
            # Créer une nouvelle inscription
            Registration.objects.create(user=request.user, activity=activite)
            messages.success(request, "Vous êtes maintenant inscrit à cette activité.")
        return redirect('activite_list')

    return render(request, 'register_for_activity.html', {'activite': activite})

@login_required
def create_activity(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        ville_id = request.POST.get('ville')
        type_id = request.POST.get('type')
        ville = Ville.objects.get(id=ville_id)
        type_activite = TypeActivite.objects.get(id=type_id)
        date = request.POST.get('date')
        activite = Activite.objects.create(
            nom=nom,
            createur=request.user,
            ville=ville,
            type=type_activite,
            date=date
        )
        return redirect('activite_list')
    
    villes = Ville.objects.all()
    types = TypeActivite.objects.all()
    return render(request, 'create_activity.html', {'villes': villes, 'types': types})

def view_registrations(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)

    # Vérifier que l'utilisateur est le créateur de l'activité
    if request.user != activite.createur:
        messages.error(request, "Vous n'avez pas la permission de voir cette liste.")
        return redirect('activite_list')

    registrations = Registration.objects.filter(activity=activite)
    return render(request, 'view_registrations.html', {'activite': activite, 'registrations': registrations})
