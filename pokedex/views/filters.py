"""Views for listing Pokémon types and abilities via REST API."""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pokedex.models import Ability, Type


class TypeListAPIView(APIView):
    """API view to list all Pokémon types."""

    def get(self, request):
        """
        Handle GET request to retrieve types.

        Queries all Type records, orders them by name, and serializes
        each into a dict with `id` and `name`.
        """
        types = Type.objects.all().order_by('name')
        data = [{'id': t.id, 'name': t.name} for t in types]
        return Response(data, status=status.HTTP_200_OK)


class AbilityListAPIView(APIView):
    """API view to list all Pokémon abilities."""

    def get(self, request):
        """
        Handle GET request to retrieve abilities.

        Queries all Ability records, orders them by name, and serializes
        each into a dict with `id` and `name`.
        """
        abilities = Ability.objects.all().order_by('name')
        data = [{'id': a.id, 'name': a.name} for a in abilities]
        return Response(data, status=status.HTTP_200_OK)
