from django.contrib import admin
from django.urls import path, include
from public import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('activites/', views.activite_list, name='activite_list'),
    path('register/<int:activite_id>/', views.inscription_activite, name='inscription_activite'),
    path('create/', views.creer_activite, name='creer_activite'),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('activites/<int:activite_id>/inscriptions/', views.inscription_activite_list, name='inscription_activite_list'),
    path('activites/<int:activite_id>/supprimer/', views.supprimer_activite, name='supprimer_activite'),
    path('api/', include('api.urls')),
]
