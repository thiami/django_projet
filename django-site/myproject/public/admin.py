from django.contrib import admin
from .models import Ville, TypeActivite, Activite, Registration



@admin.register(Ville)
class VilleAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(TypeActivite)
class TypeActiviteAdmin(admin.ModelAdmin):
    list_display = ('type',)

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'createur', 'ville', 'date')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'date')
