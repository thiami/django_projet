from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Ville(models.Model):
    nom = models.CharField(max_length=280)

class TypeActivite(models.Model):
    type = models.CharField(max_length=280)

class Activite(models.Model):
    nom = models.CharField(max_length=280)
    createur = models.ForeignKey(User, on_delete=models.CASCADE)
    ville = models.ForeignKey(Ville, on_delete=models.CASCADE)
    date = models.CharField(max_length=280)

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activite, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
