from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Activite, Ville, TypeActivite, Registration
from django.contrib.auth.models import User
from .forms import RegistrationForm  # Assure-toi que ce formulaire est défini dans forms.py

# Affiche la page d'accueil
def index(request):
    return render(request, 'index.html')

# Affiche la liste des activités
def activite_list(request):
    activites = Activite.objects.all()
    return render(request, 'activite_list.html', {'activites': activites})

# Permet à un utilisateur de s'inscrire à une activité
@login_required
def register_for_activity(request, activite_id):
    activite = get_object_or_404(Activite, id=activite_id)
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.activity = activite
            registration.save()
            return redirect('activite_list')
    else:
        form = RegistrationForm()
    
    return render(request, 'register_for_activity.html', {'form': form, 'activite': activite})

# Permet à un utilisateur de créer une nouvelle activité
@login_required
def create_activity(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        ville_id = request.POST.get('ville')
        type_id = request.POST.get('type')
        ville = get_object_or_404(Ville, id=ville_id)
        type_activite = get_object_or_404(TypeActivite, id=type_id)
        
        Activite.objects.create(
            nom=nom,
            createur=request.user,
            ville=ville,
            type=type_activite
        )
        return redirect('activite_list')
    
    villes = Ville.objects.all()
    types = TypeActivite.objects.all()
    return render(request, 'create_activity.html', {'villes': villes, 'types': types})
