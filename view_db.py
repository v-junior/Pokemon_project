"""
Pokemon Database Viewer
Author: Vilmar Junior
Project: Challenge Assignment
"""

import argparse
import json
from app import Session
from app.models import Pokemon


def list_all_pokemon():
    """Show all Pokemon in the database."""
    session = Session()
    try:
        all_pokemon = session.query(Pokemon).order_by(Pokemon.pokedex_number).all()
        
        if not all_pokemon:
            print("No Pokemon found in database.")
            print("Run 'python scout.py --default' to add some.")
            return
        
        print(f"\n{'='*60}")
        print(f"POKEMON IN DATABASE ({len(all_pokemon)} total)")
        print(f"{'='*60}\n")
        
        for p in all_pokemon:
            types = ', '.join([t.type_name for t in p.types])
            print(f"#{p.pokedex_number:03d} - {p.name:15s} | Types: {types}")
        
        print(f"\n{'='*60}\n")
        
    finally:
        session.close()


def view_pokemon(pokemon_name):
    """Show detailed info about a Pokemon."""
    session = Session()
    try:
        pokemon = session.query(Pokemon).filter_by(name=pokemon_name.capitalize()).first()
        
        if not pokemon:
            print(f"\nPokemon '{pokemon_name}' not in database.")
            print("Use --list to see what's available.")
            return
        
        print(f"\n{'='*60}")
        print(f"POKEMON DETAILS: {pokemon.name.upper()}")
        print(f"{'='*60}\n")
        
        print(f"Pokedex Number: #{pokemon.pokedex_number}")
        print(f"Height: {pokemon.height / 10:.1f}m")
        print(f"Weight: {pokemon.weight / 10:.1f}kg")
        print(f"Base Experience: {pokemon.base_experience}")
        
        print(f"\nTypes:")
        for ptype in pokemon.types:
            print(f"  - {ptype.type_name}")
        
        print(f"\nAbilities:")
        for ability in pokemon.abilities:
            hidden = " (Hidden)" if ability.is_hidden else ""
            print(f"  - {ability.ability_name}{hidden}")
        
        print(f"\nBase Stats:")
        for stat in pokemon.stats:
            bar = '█' * (stat.base_stat // 5)
            print(f"  {stat.stat_name:20s}: {stat.base_stat:3d} {bar}")
        
        if pokemon.sprite_url:
            print(f"\nSprite URL: {pokemon.sprite_url}")
        
        print(f"\n{'='*60}\n")
        
    finally:
        session.close()


def view_all_detailed():
    """View all Pokemon with full details."""
    session = Session()
    try:
        all_pokemon = session.query(Pokemon).order_by(Pokemon.pokedex_number).all()
        
        if not all_pokemon:
            print("No Pokemon found in database.")
            return
        
        for pokemon in all_pokemon:
            print(f"\n{'='*60}")
            print(f"#{pokemon.pokedex_number:03d} - {pokemon.name.upper()}")
            print(f"{'='*60}")
            
            types = ', '.join([t.type_name for t in pokemon.types])
            abilities = ', '.join([a.ability_name for a in pokemon.abilities])
            
            print(f"Types: {types}")
            print(f"Abilities: {abilities}")
            print(f"Height: {pokemon.height / 10:.1f}m | Weight: {pokemon.weight / 10:.1f}kg")
            print(f"Base Experience: {pokemon.base_experience}")
            
            print("\nStats:")
            for stat in pokemon.stats:
                print(f"  {stat.stat_name:20s}: {stat.base_stat:3d}")
        
        print(f"\n{'='*60}\n")
        print(f"Total Pokemon: {len(all_pokemon)}")
        
    finally:
        session.close()


def export_to_json(filename):
    """Export all Pokemon data to a JSON file."""
    session = Session()
    try:
        all_pokemon = session.query(Pokemon).all()
        
        if not all_pokemon:
            print("No Pokemon found in database.")
            return
        
        data = {
            'count': len(all_pokemon),
            'pokemon': [p.to_dict() for p in all_pokemon]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Exported {len(all_pokemon)} Pokemon to '{filename}'")
        
    finally:
        session.close()


def stats_summary():
    """Show database statistics."""
    session = Session()
    try:
        total = session.query(Pokemon).count()
        
        if total == 0:
            print("No Pokemon found in database.")
            return
        
        print(f"\n{'='*60}")
        print(f"DATABASE STATISTICS")
        print(f"{'='*60}\n")
        
        print(f"Total Pokemon: {total}")
        
        # Get all Pokemon with types
        from sqlalchemy import func
        from app.models import PokemonType
        
        type_counts = session.query(
            PokemonType.type_name, 
            func.count(PokemonType.type_name)
        ).group_by(PokemonType.type_name).all()
        
        print(f"\nType Distribution:")
        for type_name, count in sorted(type_counts, key=lambda x: x[1], reverse=True):
            print(f"  {type_name:15s}: {count}")
        
        # Average stats
        avg_height = session.query(func.avg(Pokemon.height)).scalar()
        avg_weight = session.query(func.avg(Pokemon.weight)).scalar()
        avg_exp = session.query(func.avg(Pokemon.base_experience)).scalar()
        
        print(f"\nAverages:")
        print(f"  Height: {avg_height / 10:.2f}m")
        print(f"  Weight: {avg_weight / 10:.2f}kg")
        print(f"  Base Experience: {avg_exp:.1f}")
        
        print(f"\n{'='*60}\n")
        
    finally:
        session.close()


def main():
    parser = argparse.ArgumentParser(
        description='View Pokemon data stored in the database'
    )
    
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--list',
        action='store_true',
        help='List all Pokemon in database'
    )
    group.add_argument(
        '--pokemon',
        type=str,
        metavar='NAME',
        help='View detailed information about a specific Pokemon'
    )
    group.add_argument(
        '--all',
        action='store_true',
        help='View all Pokemon with full details'
    )
    group.add_argument(
        '--export',
        type=str,
        metavar='FILENAME',
        help='Export all Pokemon to JSON file'
    )
    group.add_argument(
        '--stats',
        action='store_true',
        help='Show database statistics'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_all_pokemon()
    elif args.pokemon:
        view_pokemon(args.pokemon)
    elif args.all:
        view_all_detailed()
    elif args.export:
        export_to_json(args.export)
    elif args.stats:
        stats_summary()
    else:
        # Default: list all Pokemon
        list_all_pokemon()


if __name__ == '__main__':
    main()
