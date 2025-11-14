# Pokemon Scout API

**Author:** Vilmar Junior  
**Project Type:** Challenge Assignment

A Flask application that fetches and stores Pokemon data from PokeAPI. Built as a technical challenge to demonstrate skills in API integration, data processing, database design, and web development.

## Features

- **Data Retrieval**: Fetch Pokemon data from PokeAPI
- **Data Processing**: Sanitize and format raw API data into structured information
- **Database Storage**: Store Pokemon data in SQLite database using SQLAlchemy ORM
- **REST API**: Access Pokemon data through Flask REST endpoints
- **CLI Tool**: Command-line interface for batch operations
- **Interactive Menu**: User-friendly terminal menu for easy navigation
- **Reusable**: Easy to configure for any Pokemon

## Project Structure

```
Pokemon project/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── routes.py            # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── pokemon.py       # SQLAlchemy models
│   └── services/
│       ├── __init__.py
│       ├── pokeapi.py       # PokeAPI service
│       └── data_processor.py # Data sanitization
├── venv/                    # Virtual environment
├── run.py                   # Flask app runner
├── scout.py                 # CLI tool
├── menu.py                  # Interactive menu (bonus feature)
├── view_db.py               # Database viewer
├── requirements.txt         # Python dependencies
├── pokemon_list.txt         # Default Pokemon list
└── README.md               # This file
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**

   ```powershell
   git clone https://github.com/v-junior/Pokemon_project.git
   cd Pokemon_project
   ```

2. **Create and activate virtual environment**

   ```powershell
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   .\venv\Scripts\Activate.ps1
   ```

   If you encounter an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Initialize the database**

   ```powershell
   python scout.py --init-db
   ```

## Usage

### Method 1: Interactive Menu (Easiest - Bonus Feature!)

```powershell
python menu.py
```

This gives you a friendly numbered menu with all features:
- Fetch Pokemon (single or multiple)
- View database contents
- Export data to JSON
- Start API server
- Database statistics
- And more!

Perfect if you prefer a guided experience over typing commands.

### Method 2: Command-Line Interface

#### Fetch Default Pokemon List

The default list includes: Pikachu, Dhelmise, Charizard, Parasect, Aerodactyl, and Kingler.

```powershell
python scout.py --default
```

#### Fetch Specific Pokemon

```powershell
# Single Pokemon
python scout.py bulbasaur

# Multiple Pokemon
python scout.py bulbasaur squirtle charmander
```

### Method 3: Flask API

#### Start the Flask Server

```powershell
python run.py
```

The API will be available at `http://127.0.0.1:5000`

#### API Endpoints

1. **Home/Info**
   ```
   GET /
   ```
   Returns API information and available endpoints.

2. **Fetch and Store Pokemon**
   ```
   GET /api/pokemon/<name>
   ```
   Retrieves Pokemon data from PokeAPI and stores it in the database.
   
   Example:
   ```powershell
   curl http://127.0.0.1:5000/api/pokemon/pikachu
   ```

3. **List All Stored Pokemon**
   ```
   GET /api/pokemon
   ```
   Returns all Pokemon stored in the database.
   
   Example:
   ```powershell
   curl http://127.0.0.1:5000/api/pokemon
   ```

4. **Get Specific Pokemon Info**
   ```
   GET /api/pokemon/<name>/info
   ```
   Returns detailed information about a specific Pokemon from the database.
   
   Example:
   ```powershell
   curl http://127.0.0.1:5000/api/pokemon/pikachu/info
   ```

## Configuration for Other Pokemon

This application is designed to be easily reusable for any Pokemon. Here are several ways to configure it:

### Option 1: Command Line

Simply provide Pokemon names as arguments:

```powershell
python scout.py mewtwo dragonite garchomp
```

### Option 2: Edit pokemon_list.txt

1. Open `pokemon_list.txt`
2. Add Pokemon names (one per line)
3. You can then fetch them using the API or modify the CLI to read from this file

### Option 3: Use the API

Start the Flask server and make GET requests to:
```
http://127.0.0.1:5000/api/pokemon/<pokemon-name>
```

### Option 4: Batch Script

Create a PowerShell script to automate fetching multiple Pokemon:

```powershell
# fetch_pokemon.ps1
$pokemon = @('mewtwo', 'dragonite', 'garchomp', 'lucario')
foreach ($name in $pokemon) {
    python scout.py $name
}
```

## Data Structure

### Pokemon Data Stored

For each Pokemon, the following data is collected and stored:

- **Basic Info**: Name, Pokedex Number, Height, Weight, Base Experience
- **Sprite**: Official artwork URL
- **Types**: All types (e.g., Electric, Fire)
- **Abilities**: All abilities including hidden abilities
- **Stats**: HP, Attack, Defense, Special Attack, Special Defense, Speed

### Database Schema

The application uses a relational database with the following tables:

- `pokemon`: Main Pokemon information
- `pokemon_types`: Pokemon types (one-to-many)
- `pokemon_abilities`: Pokemon abilities (one-to-many)
- `pokemon_stats`: Pokemon base stats (one-to-many)

## Data Export

### Export to JSON

Export all stored Pokemon data to a JSON file:

```powershell
python view_db.py --export my_pokemon_data.json
```

This creates a JSON file with all Pokemon information including:
- Basic details (name, number, height, weight)
- Types
- Abilities
- Base stats
- Sprite URLs

The exported JSON follows this structure:
```json
{
  "count": 6,
  "pokemon": [
    {
      "name": "Pikachu",
      "pokedex_number": 25,
      "types": ["electric"],
      "abilities": ["static", "lightning-rod"],
      "stats": {
        "hp": 35,
        "attack": 55,
        "defense": 40,
        "special-attack": 50,
        "special-defense": 50,
        "speed": 90
      },
      ...
    }
  ]
}
```

You can then use this JSON file for:
- Data analysis
- Sharing with team members
- Importing into other applications
- Creating backups

## Examples

### Example 1: Fetch Default Pokemon via CLI

```powershell
python scout.py --default
```

Output:
```
Fetching default Pokemon list: pikachu, dhelmise, charizard, parasect, aerodactyl, kingler
Fetching data for pikachu...
✓ Pikachu stored successfully!
Fetching data for dhelmise...
✓ Dhelmise stored successfully!
...
```

### Example 2: Fetch Custom Pokemon via API

```powershell
# Start server
python run.py

# In another terminal (with venv activated)
curl http://127.0.0.1:5000/api/pokemon/mewtwo
```

### Example 3: View All Stored Pokemon

```powershell
curl http://127.0.0.1:5000/api/pokemon
```

## Error Handling

The app handles common issues pretty well:
- Returns 404 if Pokemon doesn't exist
- Handles API timeouts and connection problems
- Won't add duplicate Pokemon
- Validates all data before saving

## Database Location

The SQLite database is created as `pokemon_scout.db` in the project root directory.

To reset the database, simply delete `pokemon_scout.db` and run:
```powershell
python scout.py --init-db
```

## Troubleshooting

**Virtual environment not working?**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

**Missing modules?**
Make sure venv is active (you'll see `(venv)` in terminal), then:
```powershell
pip install -r requirements.txt
```

**Database errors?**
Just reinitialize it:
```powershell
python scout.py --init-db
```

## Technologies Used

- **Flask 3.0.0**: Web framework for REST API
- **SQLAlchemy 2.0.23**: ORM for database operations
- **Requests 2.31.0**: HTTP library for PokeAPI calls
- **SQLite**: Lightweight database
- **PokeAPI**: Pokemon data source

## About This Project

This project was developed by **Vilmar Junior** as a technical challenge assignment to demonstrate proficiency in:
- RESTful API development with Flask
- Data processing and sanitization
- Database design with SQLAlchemy
- Clean code architecture
- Documentation and user experience

All Pokemon data is sourced from [PokeAPI](https://pokeapi.co/). Pokemon and related content are owned by Nintendo/Game Freak/Creatures Inc.

---

**Author:** Vilmar Junior  
**Date:** November 2025  
**Purpose:** Challenge Assignment - Technical Skills Assessment  
**Repository:** https://github.com/v-junior/Pokemon_project
