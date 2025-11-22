"""
Pokemon Scout API - Main Entry Point
Author: Vilmar Junior
Project: Challenge Assignment
"""

import os
import logging

from app import app, init_db


logger = logging.getLogger(__name__)


if __name__ == '__main__':
    init_db()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s'
    )

    logger.info("Database initialized successfully!")
    logger.info("Starting Pokemon Scout API...")

    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    logger.info(f"Access the API at http://127.0.0.1:{port}")

    debug_env = os.environ.get('APP_ENV', 'development') != 'production'
    app.run(debug=debug_env, host=host, port=port)
