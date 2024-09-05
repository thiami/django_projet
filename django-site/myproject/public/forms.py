from django import forms
from .models import Registration

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = []  # Ajoute ici les champs que tu souhaites afficher dans le formulaire
