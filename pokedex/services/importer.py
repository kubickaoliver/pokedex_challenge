"""Module for importing Pokémon data from the PokéAPI into the local database."""
import logging

import requests
from django.db import transaction

from pokedex.models import Ability, EvolutionChain, Pokemon, PokemonStat, Stat, Type

from .pokeapi import PokeAPIClient

logger = logging.getLogger(__name__)


class PokedexImporter:
    """Handle importing Pokémon data into the database."""

    def __init__(self, client: PokeAPIClient):
        """
        Initialize the importer with a PokéAPI client.

        :param client: Instance of PokeAPIClient to fetch Pokémon data.
        """
        self.client = client
        self.type_cache = {}
        self.ability_cache = {}
        self.stat_cache = {}

    def _get_or_create_type(self, name):
        if name not in self.type_cache:
            obj, _ = Type.objects.get_or_create(name=name)
            self.type_cache[name] = obj
        return self.type_cache[name]

    def _get_or_create_ability(self, name):
        if name not in self.ability_cache:
            obj, _ = Ability.objects.get_or_create(name=name)
            self.ability_cache[name] = obj
        return self.ability_cache[name]

    def _get_or_create_stat(self, name):
        if name not in self.stat_cache:
            obj, _ = Stat.objects.get_or_create(name=name)
            self.stat_cache[name] = obj
        return self.stat_cache[name]

    def import_range(self, limit=None):
        """
        Import a range of Pokémon by ID into the database.

        Fetches species and evolution data, creates or updates records for
        each Pokémon up to the given limit (or all available if limit is None).

        :param limit: Maximum number of Pokémon to import (defaults to all).
        """
        total = self.client.get_total_count()
        max_id = limit if limit and limit > 0 else total
        logger.info(f"Importing up to {max_id} Pokémon (total available: {total})")

        for pid in range(1, max_id + 1):
            logger.info(f"Importing Pokémon #{pid}")
            try:
                data = self.client.get_pokemon(pid)
            except requests.HTTPError as e:
                logger.error(f"Failed to fetch Pokémon {pid}: {e}")
                continue

            with transaction.atomic():
                # Evolution chain
                species = self.client.get_species(data['species']['url'])
                evo_url = species.get('evolution_chain', {}).get('url')
                chain = None
                if evo_url:
                    evo_data = self.client.get_evolution_chain(evo_url)
                    chain, _ = EvolutionChain.objects.update_or_create(
                        chain_id=evo_data['id'],
                        defaults={'data': evo_data}
                    )

                # Pokémon
                pokemon, _ = Pokemon.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'name': data['name'],
                        'height': data['height'],
                        'weight': data['weight'],
                        'base_experience': data['base_experience'],
                        'sprite_url': data['sprites']['front_default'],
                        'evolution_chain': chain,
                    }
                )

                # Types
                pokemon.types.set(
                    [self._get_or_create_type(t['type']['name']) for t in data.get('types', [])]
                )

                # Abilities
                pokemon.abilities.set(
                    [
                        self._get_or_create_ability(a['ability']['name'])
                        for a in data.get('abilities', [])
                    ]
                )

                # Stats
                PokemonStat.objects.filter(pokemon=pokemon).delete()
                stats = []
                for s in data.get('stats', []):
                    stat_obj = self._get_or_create_stat(s['stat']['name'])
                    stats.append(
                        PokemonStat(
                            pokemon=pokemon,
                            stat=stat_obj,
                            base_stat=s['base_stat']
                        )
                    )
                PokemonStat.objects.bulk_create(stats)

        logger.info("Pokédex import complete.")