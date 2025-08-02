"""Views and API endpoints for comparing Pokémon in the Pokedex application."""
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pokedex.models import Pokemon


class PokemonCompareAPIView(APIView):
    """API view to compare two Pokémon by their IDs."""

    def get(self, request):
        """
        Handle GET requests to compare two Pokémon.

        - Validates that both `id1` and `id2` parameters are provided.
        - Fetches each Pokémon or returns 404 if not found.
        - Serializes the relevant fields for both Pokémon and returns them.
        """
        id1 = request.GET.get('id1')
        id2 = request.GET.get('id2')
        if not id1 or not id2:
            return Response(
                {'detail': 'Both id1 and id2 parameters are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            p1 = Pokemon.objects.get(id=int(id1))
            p2 = Pokemon.objects.get(id=int(id2))
        except Pokemon.DoesNotExist:
            return Response(
                {'detail': 'One or both Pokémon not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        def serialize(p):
            return {
                'id': p.id,
                'name': p.name.title(),
                'height': p.height,
                'weight': p.weight,
                'base_experience': p.base_experience,
                'types': [t.name for t in p.types.all()],
                'abilities': [a.name for a in p.abilities.all()],
                'sprite_url': p.sprite_url,
                'stats': {ps.stat.name: ps.base_stat for ps in p.pokemonstat_set.all()},
            }

        return Response(
            {'pokemon1': serialize(p1), 'pokemon2': serialize(p2)},
            status=status.HTTP_200_OK
        )

class PokemonCompareView(TemplateView):
    """Template view for the Pokémon comparison SPA frontend."""

    template_name = 'pokedex/pokemon_compare.html'
