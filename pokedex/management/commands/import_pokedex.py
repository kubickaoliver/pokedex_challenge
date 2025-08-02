"""Module for importing Pokémon data from the PokéAPI into the database."""
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from pokedex.services import PokeAPIClient, PokedexImporter

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Django management command to import Pokémon data from PokéAPI into the database."""

    help = 'Import all Pokémon data from PokéAPI into the local database.'

    def add_arguments(self, parser):
        """
        Add command-line arguments for limiting the number of Pokémon to import.

        :param parser: ArgumentParser instance to which arguments are added.
        """
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Max number of Pokémon to import (default=all available)'
        )

    def handle(self, *args, **options):
        """
        Execute the import of Pokémon data.

        Initializes the PokéAPI client and importer, sets up logging,
        and runs the import_range with the given limit.

        :param args: Positional arguments (unused).
        :param options: Dictionary of command options, expects 'limit'.
        """
        base = settings.API_BASE
        client = PokeAPIClient(base_url=base)
        importer = PokedexImporter(client=client)

        log_level = logging.INFO
        logging.basicConfig(level=log_level)

        importer.import_range(limit=options.get('limit'))
        self.stdout.write(self.style.SUCCESS('Pokédex import complete.'))