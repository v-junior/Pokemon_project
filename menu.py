import os
import sys
from app import init_db, Session
from app.services import PokeAPIService, DataProcessor
from app.models import Pokemon, PokemonType, PokemonAbility, PokemonStat
import json


class PokemonScoutMenu:
    """Interactive menu for Pokemon Scout application."""
    
    def __init__(self):
        self.pokeapi = PokeAPIService()
        self.processor = DataProcessor()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print the application header."""
        print("\n" + "="*60)
        print(" " * 15 + "🎮 POKEMON SCOUT API 🎮")
        print("="*60)
    
    def print_menu(self):
        """Display the main menu."""
        self.clear_screen()
        self.print_header()
        print("\nMAIN MENU:")
        print("\n1.  Fetch Single Pokemon")
        print("2.  Fetch Multiple Pokemon")
        print("3.  Fetch Default Pokemon List")
        print("4.  View All Pokemon in Database")
        print("5.  View Specific Pokemon Details")
        print("6.  Search Pokemon by Type")
        print("7.  Database Statistics")
        print("8.  Export Pokemon to JSON")
        print("9.  Initialize/Reset Database")
        print("10. Start Flask API Server")
        print("11. Help & Documentation")
        print("0.  Exit")
        print("\n" + "="*60)
    
    def fetch_single_pokemon(self):
        """Fetch a single Pokemon."""
        print("\n" + "-"*60)
        print("FETCH SINGLE POKEMON")
        print("-"*60)
        
        name = input("\nEnter Pokemon name: ").strip()
        
        if not name:
            print("❌ Pokemon name cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n⏳ Fetching {name}...")
        
        session = Session()
        try:
            # Check if already exists
            existing = session.query(Pokemon).filter_by(name=name.capitalize()).first()
            if existing:
                print(f"✓ {name.capitalize()} already exists in database")
                input("\nPress Enter to continue...")
                return
            
            # Fetch from API
            raw_data = self.pokeapi.get_pokemon(name)
            if not raw_data:
                print(f"❌ Failed to fetch {name}")
                input("\nPress Enter to continue...")
                return
            
            # Process data
            sanitized_data = self.processor.sanitize_pokemon_data(raw_data)
            if not sanitized_data:
                print(f"❌ Failed to process {name} data")
                input("\nPress Enter to continue...")
                return
            
            # Store in database
            pokemon = Pokemon(
                name=sanitized_data['name'],
                pokedex_number=sanitized_data['pokedex_number'],
                height=sanitized_data['height'],
                weight=sanitized_data['weight'],
                base_experience=sanitized_data['base_experience'],
                sprite_url=sanitized_data['sprite_url']
            )
            
            for type_data in sanitized_data['types']:
                pokemon.types.append(PokemonType(**type_data))
            
            for ability_data in sanitized_data['abilities']:
                pokemon.abilities.append(PokemonAbility(**ability_data))
            
            for stat_data in sanitized_data['stats']:
                pokemon.stats.append(PokemonStat(**stat_data))
            
            session.add(pokemon)
            session.commit()
            
            print(f"\n✓ {sanitized_data['name']} stored successfully!")
            print(f"   Pokedex: #{sanitized_data['pokedex_number']}")
            print(f"   Types: {', '.join([t['type_name'] for t in sanitized_data['types']])}")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Error: {e}")
        finally:
            session.close()
        
        input("\nPress Enter to continue...")
    
    def fetch_multiple_pokemon(self):
        """Fetch multiple Pokemon."""
        print("\n" + "-"*60)
        print("FETCH MULTIPLE POKEMON")
        print("-"*60)
        
        print("\nEnter Pokemon names separated by commas")
        print("Example: pikachu, charizard, mewtwo")
        names_input = input("\nPokemon names: ").strip()
        
        if not names_input:
            print("❌ No Pokemon names provided.")
            input("\nPress Enter to continue...")
            return
        
        names = [name.strip() for name in names_input.split(',')]
        
        print(f"\n⏳ Fetching {len(names)} Pokemon...\n")
        
        success_count = 0
        for name in names:
            session = Session()
            try:
                existing = session.query(Pokemon).filter_by(name=name.capitalize()).first()
                if existing:
                    print(f"⊘ {name.capitalize()} - already exists")
                    continue
                
                raw_data = self.pokeapi.get_pokemon(name)
                if not raw_data:
                    print(f"❌ {name.capitalize()} - not found")
                    continue
                
                sanitized_data = self.processor.sanitize_pokemon_data(raw_data)
                if not sanitized_data:
                    print(f"❌ {name.capitalize()} - processing failed")
                    continue
                
                pokemon = Pokemon(
                    name=sanitized_data['name'],
                    pokedex_number=sanitized_data['pokedex_number'],
                    height=sanitized_data['height'],
                    weight=sanitized_data['weight'],
                    base_experience=sanitized_data['base_experience'],
                    sprite_url=sanitized_data['sprite_url']
                )
                
                for type_data in sanitized_data['types']:
                    pokemon.types.append(PokemonType(**type_data))
                
                for ability_data in sanitized_data['abilities']:
                    pokemon.abilities.append(PokemonAbility(**ability_data))
                
                for stat_data in sanitized_data['stats']:
                    pokemon.stats.append(PokemonStat(**stat_data))
                
                session.add(pokemon)
                session.commit()
                
                print(f"✓ {sanitized_data['name']} - stored successfully")
                success_count += 1
                
            except Exception as e:
                session.rollback()
                print(f"❌ {name.capitalize()} - error: {e}")
            finally:
                session.close()
        
        print(f"\n{'='*60}")
        print(f"Successfully stored: {success_count}/{len(names)} Pokemon")
        input("\nPress Enter to continue...")
    
    def fetch_default_pokemon(self):
        """Fetch the default Pokemon list."""
        print("\n" + "-"*60)
        print("FETCH DEFAULT POKEMON LIST")
        print("-"*60)
        
        default_pokemon = ['pikachu', 'dhelmise', 'charizard', 'parasect', 'aerodactyl', 'kingler']
        
        print(f"\nDefault list: {', '.join([p.capitalize() for p in default_pokemon])}")
        confirm = input("\nProceed? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n⏳ Fetching {len(default_pokemon)} Pokemon...\n")
        
        success_count = 0
        for name in default_pokemon:
            session = Session()
            try:
                existing = session.query(Pokemon).filter_by(name=name.capitalize()).first()
                if existing:
                    print(f"⊘ {name.capitalize()} - already exists")
                    continue
                
                raw_data = self.pokeapi.get_pokemon(name)
                if not raw_data:
                    print(f"❌ {name.capitalize()} - not found")
                    continue
                
                sanitized_data = self.processor.sanitize_pokemon_data(raw_data)
                if not sanitized_data:
                    print(f"❌ {name.capitalize()} - processing failed")
                    continue
                
                pokemon = Pokemon(
                    name=sanitized_data['name'],
                    pokedex_number=sanitized_data['pokedex_number'],
                    height=sanitized_data['height'],
                    weight=sanitized_data['weight'],
                    base_experience=sanitized_data['base_experience'],
                    sprite_url=sanitized_data['sprite_url']
                )
                
                for type_data in sanitized_data['types']:
                    pokemon.types.append(PokemonType(**type_data))
                
                for ability_data in sanitized_data['abilities']:
                    pokemon.abilities.append(PokemonAbility(**ability_data))
                
                for stat_data in sanitized_data['stats']:
                    pokemon.stats.append(PokemonStat(**stat_data))
                
                session.add(pokemon)
                session.commit()
                
                print(f"✓ {sanitized_data['name']} - stored successfully")
                success_count += 1
                
            except Exception as e:
                session.rollback()
                print(f"❌ {name.capitalize()} - error: {e}")
            finally:
                session.close()
        
        print(f"\n{'='*60}")
        print(f"Successfully stored: {success_count}/{len(default_pokemon)} Pokemon")
        input("\nPress Enter to continue...")
    
    def view_all_pokemon(self):
        """View all Pokemon in database."""
        print("\n" + "-"*60)
        print("ALL POKEMON IN DATABASE")
        print("-"*60)
        
        session = Session()
        try:
            all_pokemon = session.query(Pokemon).order_by(Pokemon.pokedex_number).all()
            
            if not all_pokemon:
                print("\n❌ No Pokemon found in database.")
                print("Use option 1, 2, or 3 to fetch Pokemon first.")
            else:
                print(f"\nTotal: {len(all_pokemon)} Pokemon\n")
                for p in all_pokemon:
                    types = ', '.join([t.type_name for t in p.types])
                    print(f"#{p.pokedex_number:03d} - {p.name:15s} | Types: {types}")
        
        finally:
            session.close()
        
        input("\nPress Enter to continue...")
    
    def view_pokemon_details(self):
        """View detailed information about a specific Pokemon."""
        print("\n" + "-"*60)
        print("VIEW POKEMON DETAILS")
        print("-"*60)
        
        name = input("\nEnter Pokemon name: ").strip()
        
        if not name:
            print("❌ Pokemon name cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        session = Session()
        try:
            pokemon = session.query(Pokemon).filter_by(name=name.capitalize()).first()
            
            if not pokemon:
                print(f"\n❌ {name.capitalize()} not found in database.")
            else:
                print("\n" + "="*60)
                print(f"POKEMON DETAILS: {pokemon.name.upper()}")
                print("="*60)
                
                print(f"\nPokedex Number: #{pokemon.pokedex_number}")
                print(f"Height: {pokemon.height / 10:.1f}m")
                print(f"Weight: {pokemon.weight / 10:.1f}kg")
                print(f"Base Experience: {pokemon.base_experience}")
                
                print(f"\nTypes:")
                for ptype in pokemon.types:
                    print(f"  • {ptype.type_name}")
                
                print(f"\nAbilities:")
                for ability in pokemon.abilities:
                    hidden = " (Hidden)" if ability.is_hidden else ""
                    print(f"  • {ability.ability_name}{hidden}")
                
                print(f"\nBase Stats:")
                for stat in pokemon.stats:
                    bar = '█' * (stat.base_stat // 5)
                    print(f"  {stat.stat_name:20s}: {stat.base_stat:3d} {bar}")
        
        finally:
            session.close()
        
        input("\nPress Enter to continue...")
    
    def search_by_type(self):
        """Search Pokemon by type."""
        print("\n" + "-"*60)
        print("SEARCH POKEMON BY TYPE")
        print("-"*60)
        
        type_name = input("\nEnter type name (e.g., Fire, Water, Electric): ").strip()
        
        if not type_name:
            print("❌ Type name cannot be empty.")
            input("\nPress Enter to continue...")
            return
        
        session = Session()
        try:
            pokemon_with_type = session.query(Pokemon).join(PokemonType).filter(
                PokemonType.type_name == type_name.capitalize()
            ).all()
            
            if not pokemon_with_type:
                print(f"\n❌ No {type_name.capitalize()}-type Pokemon found in database.")
            else:
                print(f"\n{type_name.capitalize()}-type Pokemon ({len(pokemon_with_type)} found):\n")
                for p in pokemon_with_type:
                    types = ', '.join([t.type_name for t in p.types])
                    print(f"#{p.pokedex_number:03d} - {p.name:15s} | Types: {types}")
        
        finally:
            session.close()
        
        input("\nPress Enter to continue...")
    
    def show_statistics(self):
        """Show database statistics."""
        print("\n" + "-"*60)
        print("DATABASE STATISTICS")
        print("-"*60)
        
        session = Session()
        try:
            from sqlalchemy import func
            
            total = session.query(Pokemon).count()
            
            if total == 0:
                print("\n❌ No Pokemon found in database.")
            else:
                print(f"\nTotal Pokemon: {total}")
                
                # Type distribution
                type_counts = session.query(
                    PokemonType.type_name, 
                    func.count(PokemonType.type_name)
                ).group_by(PokemonType.type_name).all()
                
                print(f"\nType Distribution:")
                for type_name, count in sorted(type_counts, key=lambda x: x[1], reverse=True):
                    print(f"  {type_name:15s}: {count}")
                
                # Averages
                avg_height = session.query(func.avg(Pokemon.height)).scalar()
                avg_weight = session.query(func.avg(Pokemon.weight)).scalar()
                avg_exp = session.query(func.avg(Pokemon.base_experience)).scalar()
                
                print(f"\nAverages:")
                print(f"  Height: {avg_height / 10:.2f}m")
                print(f"  Weight: {avg_weight / 10:.2f}kg")
                print(f"  Base Experience: {avg_exp:.1f}")
        
        finally:
            session.close()
        
        input("\nPress Enter to continue...")
    
    def export_to_json(self):
        """Export Pokemon to JSON file."""
        print("\n" + "-"*60)
        print("EXPORT POKEMON TO JSON")
        print("-"*60)
        
        filename = input("\nEnter filename (default: pokemon_export.json): ").strip()
        
        if not filename:
            filename = "pokemon_export.json"
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        session = Session()
        try:
            all_pokemon = session.query(Pokemon).all()
            
            if not all_pokemon:
                print("\n❌ No Pokemon found in database.")
            else:
                data = {
                    'count': len(all_pokemon),
                    'pokemon': [p.to_dict() for p in all_pokemon]
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                print(f"\n✓ Exported {len(all_pokemon)} Pokemon to '{filename}'")
        
        finally:
            session.close()
        
        input("\nPress Enter to continue...")
    
    def initialize_database(self):
        """Initialize or reset the database."""
        print("\n" + "-"*60)
        print("INITIALIZE/RESET DATABASE")
        print("-"*60)
        
        print("\n⚠️  WARNING: This will reset the database!")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm != 'yes':
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return
        
        try:
            print("\n⏳ Initializing database...")
            init_db()
            print("✓ Database initialized successfully!")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def start_flask_server(self):
        """Start the Flask API server."""
        print("\n" + "-"*60)
        print("START FLASK API SERVER")
        print("-"*60)
        
        print("\nThis will start the Flask development server.")
        print("Access the API at: http://127.0.0.1:5000")
        print("\nPress Ctrl+C to stop the server.")
        confirm = input("\nStart server? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("Cancelled.")
            input("\nPress Enter to continue...")
            return
        
        try:
            from app import app
            init_db()
            print("\n✓ Database initialized!")
            print("⏳ Starting Flask server...\n")
            app.run(debug=True, host='0.0.0.0', port=5000)
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """Show help and documentation."""
        print("\n" + "-"*60)
        print("HELP & DOCUMENTATION")
        print("-"*60)
        
        print("\n📚 QUICK START GUIDE:")
        print("\n1. Initialize the database (Option 9)")
        print("2. Fetch Pokemon (Options 1-3)")
        print("3. View Pokemon data (Options 4-7)")
        print("4. Export data if needed (Option 8)")
        
        print("\n📖 DOCUMENTATION FILES:")
        print("  • README.md - Project overview")
        print("  • SETUP_GUIDE.md - Complete setup instructions")
        print("  • HOW_IT_WORKS.md - Detailed explanation (EN/PT)")
        
        print("\n🌐 API ENDPOINTS (when server is running):")
        print("  • GET / - API information")
        print("  • GET /api/pokemon/<name> - Fetch and store Pokemon")
        print("  • GET /api/pokemon - List all Pokemon")
        print("  • GET /api/pokemon/<name>/info - Get Pokemon details")
        
        print("\n💡 TIPS:")
        print("  • Pokemon names are case-insensitive")
        print("  • Use English names only")
        print("  • Check PokeAPI: https://pokeapi.co/")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Run the main menu loop."""
        while self.running:
            self.print_menu()
            choice = input("\nEnter your choice (0-11): ").strip()
            
            if choice == '1':
                self.fetch_single_pokemon()
            elif choice == '2':
                self.fetch_multiple_pokemon()
            elif choice == '3':
                self.fetch_default_pokemon()
            elif choice == '4':
                self.view_all_pokemon()
            elif choice == '5':
                self.view_pokemon_details()
            elif choice == '6':
                self.search_by_type()
            elif choice == '7':
                self.show_statistics()
            elif choice == '8':
                self.export_to_json()
            elif choice == '9':
                self.initialize_database()
            elif choice == '10':
                self.start_flask_server()
            elif choice == '11':
                self.show_help()
            elif choice == '0':
                self.clear_screen()
                print("\n👋 Thank you for using Pokemon Scout API!")
                print("Gotta catch 'em all!\n")
                self.running = False
            else:
                print("\n❌ Invalid choice. Please enter a number between 0-11.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    menu = PokemonScoutMenu()
    menu.run()


if __name__ == '__main__':
    main()
