"""Views for retrieving Pokémon details via REST API."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pokedex.models import Pokemon


def _flatten_chain(chain_node):
    """Traverse recursively the chain of evolutions and collects all Pokémon names."""
    names = [chain_node['species']['name'].title()]
    for evo in chain_node.get('evolves_to', []):
        names += _flatten_chain(evo)
    return names


class PokemonDetailAPIView(APIView):
    """API view to retrieve detailed information about a single Pokémon by ID."""

    def get(self, request, id):
        """
        Handle GET request to fetch a Pokémon's details.

        - Retrieves the Pokémon or returns 404 if not found.
        - Serializes core attributes, types, abilities, sprite URL.
        - Builds evolution chain list if available.
        """
        try:
            p = Pokemon.objects.get(id=id)
        except Pokemon.DoesNotExist:
            return Response(
                {'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            'id': p.id,
            'name': p.name.title(),
            'height': p.height,
            'weight': p.weight,
            'base_experience': p.base_experience,
            'types': [t.name for t in p.types.all()],
            'abilities': [a.name for a in p.abilities.all()],
            'sprite_url': p.sprite_url,
        }

        # Get Pokémon evaluation chain
        evo_json = p.get_evolution_chain()
        if evo_json and evo_json.get('chain'):
            data['evolution'] = _flatten_chain(evo_json['chain'])
        else:
            data['evolution'] = []

        return Response(
            data,
            status=status.HTTP_200_OK
        )