from django.urls import path
from .views import ListeActivites  

urlpatterns = [
    path('', ListeActivites.as_view(), name='liste_activites'),
   
]
