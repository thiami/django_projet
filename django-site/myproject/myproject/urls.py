from django.contrib import admin
from django.urls import path, include
from public import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('activites/', views.activite_list, name='activite_list'),
    path('register/<int:activite_id>/', views.register_for_activity, name='register_for_activity'),
    path('create/', views.create_activity, name='create_activity'),
    path('accounts/', include('django.contrib.auth.urls')),  # Inclure les URL d'authentification intégrées
]
