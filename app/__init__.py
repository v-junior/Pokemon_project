"""
Pokemon Scout API
Author: Vilmar Junior
Project: Challenge Assignment
"""

import os
import logging
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.pokemon import Base

# Load .env into environment for local development/testing
load_dotenv()

app = Flask(__name__)

# Configuration based on environment
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig

env = os.environ.get('APP_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
elif env == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Database configuration via env variable
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///pokemon_scout.db')
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

# Basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)


def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(engine)
    logger.info('Database tables ensured')

from app import routes
