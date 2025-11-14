"""
Pokemon Scout API - Main Entry Point
Author: Vilmar Junior
Project: Challenge Assignment
"""

from app import app, init_db

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
    print("Starting Pokemon Scout API...")
    print("Access the API at http://127.0.0.1:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
