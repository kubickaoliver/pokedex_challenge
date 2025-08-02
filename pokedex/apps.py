"""Module defining the AppConfig for the Pokedex Django application."""

import os
import sys

from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command


class PokedexConfig(AppConfig):
    """AppConfig for the Pokédex application."""

    name = 'pokedex'
    verbose_name = 'Pokedex'

    def ready(self):
        """
        Trigger Pokédex import on server startup.

        Checks the IMPORT_POKEDEX_ON_STARTUP setting and that the
        `runserver` command is being used. If the database has no
        Pokémon entries, runs the `import_pokedex` management command
        with the configured limit.
        """
        if not settings.IMPORT_POKEDEX_ON_STARTUP:
            return
        if len(sys.argv) < 2 or sys.argv[1] != 'runserver':
            return
        if os.environ.get('RUN_MAIN') != 'true':
            return

        call_command('import_pokedex', f'--limit={settings.IMPORT_POKEDEX_LIMIT}')