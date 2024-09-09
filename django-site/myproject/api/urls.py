from django.urls import path
from .views import ListeActivites
from .views import ActivitesFiltrer
urlpatterns = [
    path('activites/', ListeActivites.as_view(), name='api_liste_activites'),
    path('activites/selection/', ActivitesFiltrer.as_view(), name='activites_filtrer'),
]
