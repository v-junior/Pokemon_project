"""
Data Processor - Sanitizes and formats Pokemon data
Author: Vilmar Junior
Project: Challenge Assignment
"""

from typing import Dict, Any, List, Optional


class DataProcessor:
    """Cleans up the messy data from PokeAPI into something usable."""
    
    @staticmethod
    def sanitize_pokemon_data(raw_data: Dict[Any, Any]) -> Optional[Dict[str, Any]]:
        """Takes raw API response and extracts what we actually need."""
        if not raw_data:
            return None
        
        try:
            pokemon_data = {
                'name': raw_data.get('name', '').capitalize(),
                'pokedex_number': raw_data.get('id', 0),
                'height': raw_data.get('height', 0),
                'weight': raw_data.get('weight', 0),
                'base_experience': raw_data.get('base_experience', 0),
                'sprite_url': DataProcessor._extract_sprite(raw_data.get('sprites', {})),
                'types': DataProcessor._extract_types(raw_data.get('types', [])),
                'abilities': DataProcessor._extract_abilities(raw_data.get('abilities', [])),
                'stats': DataProcessor._extract_stats(raw_data.get('stats', []))
            }
            
            return pokemon_data
            
        except Exception as e:
            print(f"Error processing Pokemon data: {e}")
            return None
    
    @staticmethod
    def _extract_sprite(sprites: Dict[Any, Any]) -> str:
        """Get the best quality sprite available."""
        if not sprites:
            return ""
        
        # prefer official artwork, fall back to regular sprite
        return (
            sprites.get('other', {}).get('official-artwork', {}).get('front_default') or
            sprites.get('front_default', '')
        )
    
    @staticmethod
    def _extract_types(types_data: List[Dict[Any, Any]]) -> List[Dict[str, Any]]:
        """Pull out type information."""
        types = []
        for type_info in types_data:
            types.append({
                'type_name': type_info.get('type', {}).get('name', '').capitalize(),
                'slot': type_info.get('slot', 0)
            })
        return types
    
    @staticmethod
    def _extract_abilities(abilities_data: List[Dict[Any, Any]]) -> List[Dict[str, Any]]:
        """Extract abilities, including hidden ones."""
        abilities = []
        for ability_info in abilities_data:
            ability_name = ability_info.get('ability', {}).get('name', '')
            # make it look nicer - "lightning-rod" becomes "Lightning Rod"
            ability_name_formatted = ability_name.replace('-', ' ').title()
            
            abilities.append({
                'ability_name': ability_name_formatted,
                'is_hidden': ability_info.get('is_hidden', False),
                'slot': ability_info.get('slot', 0)
            })
        return abilities
    
    @staticmethod
    def _extract_stats(stats_data: List[Dict[Any, Any]]) -> List[Dict[str, Any]]:
        """Get base stats for the Pokemon."""
        stats = []
        for stat_info in stats_data:
            stat_name = stat_info.get('stat', {}).get('name', '')
            stat_name_formatted = stat_name.replace('-', ' ').upper()
            
            stats.append({
                'stat_name': stat_name_formatted,
                'base_stat': stat_info.get('base_stat', 0),
                'effort': stat_info.get('effort', 0)
            })
        return stats
