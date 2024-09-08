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
from django.contrib.auth import logout
def index(request):
    return render(request, 'index.html')

def activite_list(request):
    ville_id = request.GET.get('ville')  # Récupère l'ID de la ville depuis les paramètres de la requête
    type_id = request.GET.get('type')    # Récupère l'ID du type d'activité depuis les paramètres de la requête

    # Filtre les activités en fonction de la ville et du type d'activité sélectionnés
    activites = Activite.objects.all()

    if ville_id:
        activites = activites.filter(ville_id=ville_id)

    if type_id:
        activites = activites.filter(type_id=type_id)

    types_activites = TypeActivite.objects.all()
    villes = Ville.objects.all()

    context = {
        'types_activites': types_activites,
        'villes': villes,
        'activites': activites,
        'selected_ville': ville_id,
        'selected_type': type_id,
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
        adresse= request.POST.get('adresse')
        activite = Activite.objects.create(
            nom=nom,
            createur=request.user,
            ville=ville,
            type=type_activite,
            date=date,
            adresse=adresse,
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

def delete_activity(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)

    # Vérifier que l'utilisateur est le créateur de l'activité
    if request.user != activite.createur:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette activité.")
        return redirect('activite_list')

    if request.method == "POST":
        activite.delete()
        messages.success(request, "L'activité a été supprimée avec succès.")
        return redirect('activite_list')

    return render(request, 'confirm_delete.html', {'activite': activite})
