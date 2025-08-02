# Pokédex Challenge

A simple Django application integrating with the [PokeAPI](https://pokeapi.co/) to display Pokémon data. To leverage the ORM models, Pokémon are first imported into the database on application startup using the IMPORT_POKEDEX_ON_STARTUP feature. If you’re importing Pokémon during app startup, you need to wait until the import process finishes before using the app.

## Features
- List of Pokémon with pagination
- Pokémon detail view (stats, types, abilities, evolution chain)
- Search and filter by name or type
- Pokémon comparison

## Setup
1. Clone the repo:
   ```bash
    git clone <repo-url> && cd django-pokedex
    ```
2. Create and activate virtualenv (Requires Python 3.12):
   ```bash
    python -m venv .venv && source .venv/bin/activate
    ```
3. Install dependencies:
   ```bash
    pip install -r requirements.txt
    ```
4. Create `.env` file with:
   ```ini
    DEBUG=True
   
    API_BASE=https://pokeapi.co/api/v2
    ALLOWED_HOSTS=0.0.0.0,127.0.0.1,localhost
   
    IMPORT_POKEDEX_ON_STARTUP=True  # True if you need to import Pokémons to DB
    IMPORT_POKEDEX_LIMIT=100  # Number of Pokémons you want to import
    ```
5. Run migrations and start server:
   ```bash
    python manage.py migrate
    python manage.py runserver
    ```

## Docker
1. Create `.env` file with:
   ```ini
    DEBUG=False
   
    API_BASE=https://pokeapi.co/api/v2
    ALLOWED_HOSTS=0.0.0.0,127.0.0.1,localhost
   
    IMPORT_POKEDEX_ON_STARTUP=True  # True if you need to import Pokémons to DB
    IMPORT_POKEDEX_LIMIT=100  # Number of Pokémons you want to import
    ```

2. Build and run with Docker Compose:
    ```bash
    docker-compose up --build -d
    ```

## Tests
1. Run Pokédex tests:
   ```bash
    python manage.py test pokedex
    ```
## Formatting
1. Run Ruff formatter:
   ```bash
    ruff . --fix
    ```