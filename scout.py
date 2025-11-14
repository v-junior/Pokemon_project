"""
Pokemon Scout CLI - Command Line Interface
Author: Vilmar Junior
Project: Challenge Assignment
"""

import sys
import argparse
from app import init_db, Session
from app.services import PokeAPIService, DataProcessor
from app.models import Pokemon, PokemonType, PokemonAbility, PokemonStat


def fetch_and_store_pokemon(pokemon_name):
    """Fetch a Pokemon and save it to the database."""
    pokeapi = PokeAPIService()
    processor = DataProcessor()
    session = Session()
    
    try:
        print(f"Fetching data for {pokemon_name}...")
        
        # skip if we already have it
        existing = session.query(Pokemon).filter_by(name=pokemon_name.capitalize()).first()
        if existing:
            print(f"{pokemon_name.capitalize()} already exists in database")
            return True
        
        raw_data = pokeapi.get_pokemon(pokemon_name)
        if not raw_data:
            print(f"Failed to fetch {pokemon_name}")
            return False
        
        sanitized_data = processor.sanitize_pokemon_data(raw_data)
        if not sanitized_data:
            print(f"Failed to process {pokemon_name} data")
            return False
        
        pokemon = Pokemon(
            name=sanitized_data['name'],
            pokedex_number=sanitized_data['pokedex_number'],
            height=sanitized_data['height'],
            weight=sanitized_data['weight'],
            base_experience=sanitized_data['base_experience'],
            sprite_url=sanitized_data['sprite_url']
        )
        
        for type_data in sanitized_data['types']:
            pokemon.types.append(PokemonType(**type_data))
        
        for ability_data in sanitized_data['abilities']:
            pokemon.abilities.append(PokemonAbility(**ability_data))
        
        for stat_data in sanitized_data['stats']:
            pokemon.stats.append(PokemonStat(**stat_data))
        
        session.add(pokemon)
        session.commit()
        
        print(f"✓ {sanitized_data['name']} stored successfully!")
        return True
        
    except Exception as e:
        session.rollback()
        print(f"Error storing {pokemon_name}: {e}")
        return False
        
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(
        description='Pokemon Scout - Fetch Pokemon data from PokeAPI'
    )
    parser.add_argument(
        'pokemon',
        nargs='*',
        help='Pokemon names (space-separated)'
    )
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize the database'
    )
    parser.add_argument(
        '--default',
        action='store_true',
        help='Fetch default Pokemon list'
    )
    
    args = parser.parse_args()
    
    if args.init_db or not args.pokemon and not args.default:
        print("Initializing database...")
        init_db()
        print("Database initialized!")
    
    if args.default:
        default_pokemon = ['pikachu', 'dhelmise', 'charizard', 'parasect', 'aerodactyl', 'kingler']
        print(f"Fetching default Pokemon list: {', '.join(default_pokemon)}")
        for name in default_pokemon:
            fetch_and_store_pokemon(name)
    elif args.pokemon:
        for name in args.pokemon:
            fetch_and_store_pokemon(name)
    elif not args.init_db:
        parser.print_help()


if __name__ == '__main__':
    main()
