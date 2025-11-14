"""
PokeAPI Service - Handles API communication
Author: Vilmar Junior
Project: Challenge Assignment
"""

import requests
from typing import Optional, Dict, Any


class PokeAPIService:
    BASE_URL = "https://pokeapi.co/api/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Pokemon-Scout-App/1.0'
        })
    
    def get_pokemon(self, pokemon_name: str) -> Optional[Dict[Any, Any]]:
        """Fetch Pokemon data from PokeAPI."""
        try:
            pokemon_name = pokemon_name.lower().strip()
            url = f"{self.BASE_URL}/pokemon/{pokemon_name}"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Pokemon '{pokemon_name}' not found in PokeAPI")
            else:
                print(f"HTTP error occurred: {e}")
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for '{pokemon_name}': {e}")
            return None
    
    def get_pokemon_species(self, pokemon_id: int) -> Optional[Dict[Any, Any]]:
        """Fetch Pokemon species data - useful for additional info like descriptions."""
        try:
            url = f"{self.BASE_URL}/pokemon-species/{pokemon_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching species data for Pokemon ID {pokemon_id}: {e}")
            return None
