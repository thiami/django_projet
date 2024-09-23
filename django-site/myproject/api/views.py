from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from public.models import Activite, Ville, TypeActivite
from .models import ActiviteSerializer
from rest_framework import generics

class ListeActivites(APIView):
    
    def get(self, request):
        
        queryset = Activite.objects.all()
        ville_nom = request.query_params.get('ville', None)
        type_nom = request.query_params.get('type', None)

       
        if ville_nom:
            try:
                ville = Ville.objects.get(nom=ville_nom)
                queryset = queryset.filter(ville=ville)
            except Ville.DoesNotExist:
                return Response({"message": "Ville non trouvée."}, status=status.HTTP_404_NOT_FOUND)

        if type_nom:
            try:
                type_activite = TypeActivite.objects.get(type=type_nom)
                queryset = queryset.filter(type=type_activite)
            except TypeActivite.DoesNotExist:
                return Response({"message": "Type d'activité non trouvé."}, status=status.HTTP_404_NOT_FOUND)

        # Sérialisation :
        serializer = ActiviteSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
