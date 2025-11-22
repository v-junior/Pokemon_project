import pytest

from app.services.data_processor import DataProcessor


def sample_raw_pokemon():
    return {
        'name': 'pikachu',
        'id': 25,
        'height': 4,
        'weight': 60,
        'base_experience': 112,
        'sprites': {
            'other': {
                'official-artwork': {'front_default': 'https://example.com/pikachu.png'}
            },
            'front_default': 'https://example.com/front.png'
        },
        'types': [
            {'slot': 1, 'type': {'name': 'electric'}}
        ],
        'abilities': [
            {'is_hidden': False, 'slot': 1, 'ability': {'name': 'static'}},
            {'is_hidden': True, 'slot': 3, 'ability': {'name': 'lightning-rod'}}
        ],
        'stats': [
            {'base_stat': 35, 'effort': 0, 'stat': {'name': 'hp'}},
            {'base_stat': 55, 'effort': 0, 'stat': {'name': 'attack'}}
        ]
    }


def test_sanitize_happy_path():
    raw = sample_raw_pokemon()
    processed = DataProcessor.sanitize_pokemon_data(raw)

    assert processed is not None
    assert processed['name'] == 'Pikachu'
    assert processed['pokedex_number'] == 25
    assert processed['sprite_url'] == 'https://example.com/pikachu.png'
    assert len(processed['types']) == 1
    assert processed['types'][0]['type_name'] == 'Electric'
    assert any(a['ability_name'] == 'Lightning Rod' for a in processed['abilities'])
    assert any(s['stat_name'] == 'HP' for s in processed['stats'])


def test_sanitize_handles_empty():
    assert DataProcessor.sanitize_pokemon_data(None) is None
