"""URL configuration for the project, including admin and API docs."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pokedex.urls')),
]
