from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from public.models import Activite, Ville, TypeActivite
from .models import ActiviteSerializer
from rest_framework import generics

class ListeActivites(APIView):
    def get(self, request):
        activites = Activite.objects.all()
        serializer = ActiviteSerializer(activites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ActivitesFiltrer(generics.ListAPIView):
    serializer_class = ActiviteSerializer

    def get_queryset(self):
        queryset = Activite.objects.all()
        
        # Récupérer les paramètres de ville et de type depuis la requête
        ville_nom = self.request.query_params.get('ville', None)
        type_nom = self.request.query_params.get('type', None)
        
        # Filtrer par nom de ville si fourni
        if ville_nom:
            try:
                ville = Ville.objects.get(nom=ville_nom)
                queryset = queryset.filter(ville=ville)
            except Ville.DoesNotExist:
                return queryset.none()  # Si la ville n'existe pas, renvoie un queryset vide

        # Filtrer par nom de type d'activité si fourni
        if type_nom:
            try:
                type_activite = TypeActivite.objects.get(type=type_nom)
                queryset = queryset.filter(type=type_activite)
            except TypeActivite.DoesNotExist:
                return queryset.none()  # Si le type n'existe pas, renvoie un queryset vide
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({"message": "Aucune activité trouvée pour les filtres donnés."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
