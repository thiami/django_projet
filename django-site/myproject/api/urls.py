from django.urls import path
from .views import ListeActivites
from .views import ActivitesFiltrer
urlpatterns = [
    path('', ListeActivites.as_view(), name='api_liste_activites'),
    path('filter/', ActivitesFiltrer.as_view(), name='activites_filtrer'),
]
