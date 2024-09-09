from rest_framework import serializers
from public.models import Activite, Registration

class ActiviteSerializer(serializers.ModelSerializer):
    ville = serializers.StringRelatedField()  # Utilise le nom de la ville 
    type = serializers.StringRelatedField()  
    createur = serializers.StringRelatedField()  

    class Meta:
        model = Activite
        fields = ['nom', 'ville', 'type', 'date', 'adresse', 'createur']


class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    
    class Meta:
        model = Registration
        fields = ['user', 'activite', 'date']