"""Tests for the Pokedex API endpoints."""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pokedex.models import Ability, Pokemon, Type


class TestPokemonListAPI(APITestCase):
    """Test cases for the Pokémon list API endpoint."""

    @classmethod
    def setUpTestData(cls):
        """Create test data: two types, one ability, and three Pokémon entries."""
        # Create two types and one ability
        fire = Type.objects.create(name="fire")
        water = Type.objects.create(name="water")
        overgrow = Ability.objects.create(name="overgrow")

        # Create three Pokémon and assign types/abilities
        p1 = Pokemon.objects.create(
            id=1,
            name="charmander",
            height=6,
            weight=85,
            base_experience=62
        )
        p1.types.add(fire)
        p1.abilities.add(overgrow)

        p2 = Pokemon.objects.create(
            id=2,
            name="squirtle",
            height=5,
            weight=90,
            base_experience=63
        )
        p2.types.add(water)
        p2.abilities.add(overgrow)

        p3 = Pokemon.objects.create(
            id=3,
            name="bulbasaur",
            height=7,
            weight=100,
            base_experience=64
        )
        p3.types.add(water, fire)
        p3.abilities.add(overgrow)

    def test_list_returns_all_pokemon(self):
        """When no filters are applied, the endpoint should return all created Pokémon."""
        url = reverse('api-pokemon-list')
        response = self.client.get(url, {'page': 1, 'limit': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect 3 total
        self.assertEqual(response.data['count'], 3)
        returned_names = [p['name'].lower() for p in response.data['results']]
        self.assertCountEqual(returned_names, ['charmander', 'squirtle', 'bulbasaur'])

    def test_filter_by_type_and_search(self):
        """Applying a type filter and a search string should narrow the results correctly."""
        url = reverse('api-pokemon-list')

        # Filter by type "fire": should return Charmander and Bulbasaur
        response = self.client.get(url, {
            'page': 1,
            'limit': 10,
            'type': 'fire'
        })
        self.assertEqual(response.data['count'], 2)
        names_fire = [p['name'].lower() for p in response.data['results']]
        self.assertCountEqual(names_fire, ['charmander', 'bulbasaur'])

        # Search for "squi": should return only Squirtle
        response = self.client.get(url, {
            'page': 1,
            'limit': 10,
            'search': 'squi'
        })
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'].lower(), 'squirtle')


class TestPokemonCompareAPI(APITestCase):
    """Test cases for the Pokémon compare API endpoint."""

    @classmethod
    def setUpTestData(cls):
        """Create two Pokémon entries for comparison tests."""
        # Create two Pokémon for comparison
        Pokemon.objects.create(
            id=10,
            name="pikachu",
            height=4,
            weight=60,
            base_experience=112
        )
        Pokemon.objects.create(
            id=25,
            name="raichu",
            height=8,
            weight=300,
            base_experience=218
        )

    def test_compare_requires_both_ids(self):
        """The compare endpoint should return 400 if either id1 or id2 is missing."""
        url = reverse('api-pokemon-compare')
        response = self.client.get(url, {'id1': 10})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_compare_successful(self):
        """Providing two valid, distinct IDs should return detailed data for both Pokémon."""
        url = reverse('api-pokemon-compare')
        response = self.client.get(url, {'id1': 10, 'id2': 25})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The response must include both pokemon1 and pokemon2 keys
        self.assertIn('pokemon1', response.data)
        self.assertIn('pokemon2', response.data)
        # Check that the names are capitalized as expected
        self.assertEqual(response.data['pokemon1']['name'], 'Pikachu')
        self.assertEqual(response.data['pokemon2']['name'], 'Raichu')