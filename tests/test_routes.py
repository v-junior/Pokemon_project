import os

import pytest


# Ensure tests use an in-memory database and testing config
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
os.environ['APP_ENV'] = 'testing'


def sample_raw_pokemon():
    return {
        'name': 'pikachu',
        'id': 25,
        'height': 4,
        'weight': 60,
        'base_experience': 112,
        'sprites': {'front_default': 'https://example.com/front.png'},
        'types': [{'slot': 1, 'type': {'name': 'electric'}}],
        'abilities': [{'is_hidden': False, 'slot': 1, 'ability': {'name': 'static'}}],
        'stats': [{'base_stat': 35, 'effort': 0, 'stat': {'name': 'hp'}}]
    }


@pytest.fixture()
def client(monkeypatch):
    # import after environment variables set
    from app import app, init_db, engine, Base
    from app import routes as routes_module

    # Clean and recreate tables for each test
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with app.test_client() as c:
        yield c


def test_get_and_store_pokemon_success(client, monkeypatch):
    from app import routes as routes_module

    monkeypatch.setattr(routes_module.pokeapi_service, 'get_pokemon', lambda name: sample_raw_pokemon())

    resp = client.get('/api/pokemon/pikachu')
    assert resp.status_code == 201
    data = resp.get_json()
    assert 'saved successfully' in data['message']
    assert data['data']['name'] == 'Pikachu'


def test_get_and_store_pokemon_not_found(client, monkeypatch):
    from app import routes as routes_module

    monkeypatch.setattr(routes_module.pokeapi_service, 'get_pokemon', lambda name: None)

    resp = client.get('/api/pokemon/unknownmon')
    assert resp.status_code == 404
    data = resp.get_json()
    assert 'error' in data
