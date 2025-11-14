"""
Database Models - SQLAlchemy ORM Models
Author: Vilmar Junior
Project: Challenge Assignment
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Pokemon(Base):
    __tablename__ = 'pokemon'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False, index=True)
    pokedex_number = Column(Integer, nullable=False)
    height = Column(Integer)
    weight = Column(Integer)
    base_experience = Column(Integer)
    sprite_url = Column(String)
    
    types = relationship("PokemonType", back_populates="pokemon", cascade="all, delete-orphan")
    abilities = relationship("PokemonAbility", back_populates="pokemon", cascade="all, delete-orphan")
    stats = relationship("PokemonStat", back_populates="pokemon", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Pokemon(name='{self.name}', pokedex_number={self.pokedex_number})>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pokedex_number': self.pokedex_number,
            'height': self.height,
            'weight': self.weight,
            'base_experience': self.base_experience,
            'sprite_url': self.sprite_url,
            'types': [t.to_dict() for t in self.types],
            'abilities': [a.to_dict() for a in self.abilities],
            'stats': [s.to_dict() for s in self.stats]
        }


class PokemonType(Base):
    __tablename__ = 'pokemon_types'
    
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    type_name = Column(String, nullable=False)
    slot = Column(Integer)
    
    pokemon = relationship("Pokemon", back_populates="types")
    
    def __repr__(self):
        return f"<PokemonType(type='{self.type_name}')>"
    
    def to_dict(self):
        return {
            'type': self.type_name,
            'slot': self.slot
        }


class PokemonAbility(Base):
    __tablename__ = 'pokemon_abilities'
    
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    ability_name = Column(String, nullable=False)
    is_hidden = Column(Integer, default=0)
    slot = Column(Integer)
    
    pokemon = relationship("Pokemon", back_populates="abilities")
    
    def __repr__(self):
        return f"<PokemonAbility(ability='{self.ability_name}', hidden={bool(self.is_hidden)})>"
    
    def to_dict(self):
        return {
            'ability': self.ability_name,
            'is_hidden': bool(self.is_hidden),
            'slot': self.slot
        }


class PokemonStat(Base):
    __tablename__ = 'pokemon_stats'
    
    id = Column(Integer, primary_key=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    stat_name = Column(String, nullable=False)
    base_stat = Column(Integer, nullable=False)
    effort = Column(Integer, default=0)
    
    pokemon = relationship("Pokemon", back_populates="stats")
    
    def __repr__(self):
        return f"<PokemonStat(stat='{self.stat_name}', value={self.base_stat})>"
    
    def to_dict(self):
        return {
            'stat': self.stat_name,
            'base_stat': self.base_stat,
            'effort': self.effort
        }
