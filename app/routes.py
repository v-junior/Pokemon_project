"""
API Routes - RESTful Endpoints
Author: Vilmar Junior
Project: Challenge Assignment
"""

from flask import jsonify, request
from app import app, Session, init_db
from app.models import Pokemon, PokemonType, PokemonAbility, PokemonStat
from app.services import PokeAPIService, DataProcessor


pokeapi_service = PokeAPIService()
data_processor = DataProcessor()


@app.route('/')
def index():
    """Basic info about the API."""
    return jsonify({
        'message': 'Pokemon Scout API',
        'version': '1.0',
        'endpoints': {
            '/api/pokemon/<name>': 'GET - Fetch and store Pokemon',
            '/api/pokemon': 'GET - List all Pokemon',
            '/api/pokemon/<name>/info': 'GET - Get Pokemon details'
        }
    })


@app.route('/api/pokemon/<string:name>', methods=['GET'])
def get_and_store_pokemon(name):
    """Fetch Pokemon from PokeAPI and save to database."""
    session = Session()
    
    try:
        # check if we already have it
        existing_pokemon = session.query(Pokemon).filter_by(name=name.capitalize()).first()
        if existing_pokemon:
            return jsonify({
                'message': f'{name.capitalize()} already in database',
                'data': existing_pokemon.to_dict()
            }), 200
        
        raw_data = pokeapi_service.get_pokemon(name)
        
        if not raw_data:
            return jsonify({
                'error': f'Pokemon {name} not found'
            }), 404
        
        sanitized_data = data_processor.sanitize_pokemon_data(raw_data)
        
        if not sanitized_data:
            return jsonify({
                'error': 'Failed to process data'
            }), 500
        
        # create the main pokemon record
        pokemon = Pokemon(
            name=sanitized_data['name'],
            pokedex_number=sanitized_data['pokedex_number'],
            height=sanitized_data['height'],
            weight=sanitized_data['weight'],
            base_experience=sanitized_data['base_experience'],
            sprite_url=sanitized_data['sprite_url']
        )
        
        for type_data in sanitized_data['types']:
            pokemon_type = PokemonType(**type_data)
            pokemon.types.append(pokemon_type)
        
        for ability_data in sanitized_data['abilities']:
            pokemon_ability = PokemonAbility(**ability_data)
            pokemon.abilities.append(pokemon_ability)
        
        for stat_data in sanitized_data['stats']:
            pokemon_stat = PokemonStat(**stat_data)
            pokemon.stats.append(pokemon_stat)
        
        session.add(pokemon)
        session.commit()
        
        return jsonify({
            'message': f'{pokemon.name} saved successfully',
            'data': pokemon.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500
        
    finally:
        session.close()


@app.route('/api/pokemon', methods=['GET'])
def list_pokemon():
    """List all Pokemon stored in the database."""
    session = Session()
    
    try:
        all_pokemon = session.query(Pokemon).all()
        
        return jsonify({
            'count': len(all_pokemon),
            'pokemon': [p.to_dict() for p in all_pokemon]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500
        
    finally:
        session.close()


@app.route('/api/pokemon/<string:name>/info', methods=['GET'])
def get_pokemon_info(name):
    """Get detailed information about a specific Pokemon from the database."""
    session = Session()
    
    try:
        pokemon = session.query(Pokemon).filter_by(name=name.capitalize()).first()
        
        if not pokemon:
            return jsonify({
                'error': f'Pokemon {name} not found in database'
            }), 404
        
        return jsonify(pokemon.to_dict()), 200
        
    except Exception as e:
        return jsonify({
            'error': f'An error occurred: {str(e)}'
        }), 500
        
    finally:
        session.close()
