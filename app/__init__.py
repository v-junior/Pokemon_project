"""
Pokemon Scout API
Author: Vilmar Junior
Project: Challenge Assignment
"""

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pokemon import Base

app = Flask(__name__)

DATABASE_URL = "sqlite:///pokemon_scout.db"
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(engine)

from app import routes
