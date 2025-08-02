"""Module defining Pokémon-related models for the Pokedex application."""

from django.db import models


class Type(models.Model):
    """Represent a Pokémon type (e.g., Fire, Water, Grass)."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        """Meta options for Type model: default ordering by name."""

        ordering = ['name']

    def __str__(self):
        """Return the name of the type."""
        return self.name


class Ability(models.Model):
    """Represent a Pokémon ability (e.g., Overgrow, Blaze, Torrent)."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """Meta options for Ability model: default ordering by name."""

        ordering = ['name']

    def __str__(self):
        """Return the name of the ability."""
        return self.name


class Stat(models.Model):
    """Represent a Pokémon stat (e.g., HP, Attack, Defense)."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        """Meta options for Stat model: default ordering by name."""

        ordering = ['name']

    def __str__(self):
        """Return the name of the stat."""
        return self.name


class EvolutionChain(models.Model):
    """Store the full evolution chain data for a Pokémon species."""

    chain_id = models.PositiveIntegerField(primary_key=True)
    data = models.JSONField()

    def __str__(self):
        """Return a readable identifier for the evolution chain."""
        return f"EvolutionChain {self.chain_id}"


class Pokemon(models.Model):
    """Represent a Pokémon entry with all its core attributes."""

    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    base_experience = models.IntegerField()
    sprite_url = models.URLField(blank=True, default="")
    types = models.ManyToManyField(Type, related_name='pokemon')
    abilities = models.ManyToManyField(Ability, related_name='pokemon')
    stats = models.ManyToManyField(Stat, through='PokemonStat')
    evolution_chain = models.ForeignKey(
        EvolutionChain,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='pokemons'
    )

    class Meta:
        """Meta options for Pokemon model: default ordering by ID."""

        ordering = ['id']

    def __str__(self):
        """Return the Pokémon’s name in title case."""
        return self.name.title()

    def get_evolution_chain(self):
        """Return the raw evolution chain JSON data, or an empty dict."""
        return self.evolution_chain.data if self.evolution_chain else {}


class PokemonStat(models.Model):
    """Through model linking Pokémon to their stats and base stat values."""

    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
    base_stat = models.IntegerField()

    class Meta:
        """Meta options for PokemonStat: enforce unique (pokemon, stat) pairs."""

        unique_together = (('pokemon', 'stat'),)

    def __str__(self):
        """Return a string like "pikachu: speed=90"."""
        return f"{self.pokemon.name}: {self.stat.name}={self.base_stat}"
