"""Views for listing and rendering the Pokédex frontend and REST API."""
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pokedex.models import Pokemon


class PokemonListAPIView(APIView):
    """API view to list and filter Pokémon entries."""

    def get(self, request):
        """
        Handle GET requests to retrieve a paginated list of Pokémon.

        Query parameters:
        - page (int): page number (default=1)
        - limit (int): items per page (default=20)
        - search (str): substring to match in Pokémon names
        - type (list of str): filter by Pokémon type names
        - ability (list of str): filter by Pokémon ability names

        Returns JSON with 'results' (list of {'id', 'name'}) and 'count' (total matches).
        """
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 20))
        offset = (page - 1) * limit
        search = request.GET.get('search', '').strip()
        types = request.GET.getlist('type')
        abilities = request.GET.getlist('ability')
     
        qs = Pokemon.objects.all()
        if search:
            qs = qs.filter(name__icontains=search)
        if types:
            qs = qs.filter(types__name__in=types)
        if abilities:
            qs = qs.filter(abilities__name__in=abilities)
            qs = qs.distinct()
        total_count = qs.count()
        pokemons = qs[offset:offset + limit]
        results = [{'id': p.id, 'name': p.name.title()} for p in pokemons]

        return Response(
            {'results': results, 'count': total_count},
            status=status.HTTP_200_OK
        )

class PokedexView(TemplateView):
    """Template view for the Pokédex single-page application frontend."""

    template_name = 'pokedex/index.html'
