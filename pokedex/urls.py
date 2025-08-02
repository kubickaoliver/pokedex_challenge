"""URL routes for the Pokedex application."""
from django.urls import path

from pokedex import views

urlpatterns = [
    # SPA Frontend
    path('', views.PokedexView.as_view(), name='pokedex-home'),
    path('compare/', views.PokemonCompareView.as_view(), name='pokemon-compare'),

    # REST API endpoints
    path('api/pokemon/', views.PokemonListAPIView.as_view(), name='api-pokemon-list'),
    path('api/pokemon/<int:id>/', views.PokemonDetailAPIView.as_view(), name='api-pokemon-detail'),
    path('api/pokemon/compare/', views.PokemonCompareAPIView.as_view(), name='api-pokemon-compare'),
    path('api/types/', views.TypeListAPIView.as_view(),    name='api-type-list'),
    path('api/abilities/', views.AbilityListAPIView.as_view(), name='api-ability-list'),
]
