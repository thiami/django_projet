from django.contrib.auth.decorators import login_required
from .models import Activite, Ville, TypeActivite, Registration
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.http import JsonResponse
import requests
def index(request):
    return render(request, 'index.html')

def activite_list(request):
    ville_id = request.GET.get('ville')  
    type_id = request.GET.get('type')    

    
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
def inscription_activite(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)

    if request.method == 'POST':
        
        if Registration.objects.filter(user=request.user, activity=activite).exists():
            messages.warning(request, "Vous êtes déjà inscrit à cette activité.")
        else:
            
            Registration.objects.create(user=request.user, activity=activite)
            messages.success(request, "Vous êtes maintenant inscrit à cette activité.")
        return redirect('activite_list')

    return render(request, 'inscription_activite.html', {'activite': activite})

@login_required
def creer_activite(request):
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
    return render(request, 'creer_activite.html', {'villes': villes, 'types': types})

def inscription_activite_list(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)
    registrations = Registration.objects.filter(activity=activite)

    return render(request, 'inscription_activite_list.html', {'activite': activite, 'registrations': registrations})

def supprimer_activite(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)

    if request.method == "POST":
        activite.delete()
        messages.success(request, "L'activité a été supprimée avec succès.")
        return redirect('activite_list')

    return render(request, 'supprimer_activite.html', {'activite': activite})

def requetes_api(request):
    
        response = requests.get('http://api:8000/api/') 
        
        if response.status_code == 200:
            try:
                data = response.json()  
            except ValueError:
                data = {'error': 'Erreur de parsing JSON'}
        else:
            data = {'error': 'Impossible de récupérer les activités'}

        return JsonResponse(data, safe=False)  

   