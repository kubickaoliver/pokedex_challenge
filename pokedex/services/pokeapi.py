"""Module for interacting with the PokéAPI, providing a retry-enabled HTTP client."""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class PokeAPIClient:
    """Client to fetch data from the PokéAPI with retry and session pooling."""

    def __init__(self, base_url, timeout=5, max_retries=3, backoff_factor=0.3):
        """
        Initialize the PokeAPIClient.

        :param base_url: Base URL of the PokéAPI.
        :param timeout: Request timeout in seconds (default: 5)
        :param max_retries: Number of retry attempts for failed requests (default: 3)
        :param backoff_factor: Backoff factor between retry attempts (default: 0.3)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.timeout = timeout

    def fetch_json(self, path):
        """
        Perform a GET request to the given API path and return JSON data.

        :param path: API path or endpoint (relative to base_url)
        :return: Parsed JSON response
        :raises HTTPError: On request failure
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = self.session.get(url, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def get_total_count(self):
        """
        Retrieve the total number of available Pokémon entries from the API.

        :return: Total count of Pokémon
        """
        data = self.fetch_json('/pokemon?limit=1')
        return data.get('count', 0)

    def get_pokemon(self, pokemon_id):
        """
        Fetch the data for a specific Pokémon by its ID.

        :param pokemon_id: Numeric ID of the Pokémon
        :return: JSON data for the Pokémon
        """
        return self.fetch_json(f'/pokemon/{pokemon_id}')

    def get_species(self, species_url):
        """
        Fetch the species data from a full URL.

        :param species_url: Full URL to the species endpoint
        :return: JSON data for the species
        """
        return self.session.get(species_url, timeout=self.timeout).json()

    def get_evolution_chain(self, evo_url):
        """
        Fetch the evolution chain data from a full URL.

        :param evo_url: Full URL to the evolution chain endpoint
        :return: JSON data for the evolution chain
        """
        return self.session.get(evo_url, timeout=self.timeout).json()