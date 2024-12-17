import random
from .pokemon import Pokemon
from .data.pokemon_data import POKEMON_DATA

class PokemonFactory:
    def __init__(self):
        self.available_pokemon = list(POKEMON_DATA.keys())
    
    def create_pokemon(self, species=None, level=None):
        """创建一个宝可梦实例"""
        if species is None:
            species = random.choice(self.available_pokemon)
        
        if level is None:
            level = random.randint(1, 15)
        
        pokemon_data = POKEMON_DATA[species]
        
        return Pokemon(
            name=pokemon_data['name'],
            species=species,
            level=level
        )
    
    def create_wild_pokemon(self, player_level):
        """创建野生宝可梦，等级基于玩家宝可梦的等级"""
        min_level = max(1, player_level - 3)
        max_level = player_level + 2
        level = random.randint(min_level, max_level)
        
        species = random.choice(self.available_pokemon)
        return self.create_pokemon(species=species, level=level)
    
    def create_gym_pokemon(self, gym_level):
        """创建道馆宝可梦，比玩家等级稍高"""
        level = gym_level + 2
        species = random.choice(self.available_pokemon)
        return self.create_pokemon(species=species, level=level)