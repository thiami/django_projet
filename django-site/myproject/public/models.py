# public/models.py
from django.db import models
from django.contrib.auth.models import User

class Ville(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class TypeActivite(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)   # Assurez-vous que ce champ existe
    
    def __str__(self):
        return self.type

class Activite(models.Model):
    nom = models.CharField(max_length=280)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    type = models.ForeignKey(TypeActivite, on_delete=models.CASCADE)
    date = models.DateTimeField()
    adresse = models.CharField(max_length=280, null=True)
    def __str__(self):
        return self.nom

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activite, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity.nom}"
