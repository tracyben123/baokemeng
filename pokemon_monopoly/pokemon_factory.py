from pokemon import Pokemon
from move import Move, BASIC_MOVES
from pokemon_data import POKEMON_DATA, MOVE_DATA

class PokemonFactory:
    @staticmethod
    def create_pokemon(pokemon_id, level=1):
        """创建一个新的宝可梦实例"""
        if pokemon_id not in POKEMON_DATA:
            raise ValueError(f"未知的宝可梦ID: {pokemon_id}")
            
        data = POKEMON_DATA[pokemon_id]
        pokemon = Pokemon(data['name'], data['type'], level)
        
        # 设置基础属性
        base_stats = data['base_stats']
        pokemon.max_hp = base_stats['hp'] + level * 2
        pokemon.hp = pokemon.max_hp
        pokemon.attack = base_stats['attack'] + level
        pokemon.defense = base_stats['defense'] + level
        
        # 添加技能
        for move_id in data['moves']:
            if move_id in MOVE_DATA:
                move_data = MOVE_DATA[move_id]
                move = Move(
                    move_data['name'],
                    move_data['type'],
                    move_data['power'],
                    move_data['accuracy']
                )
                pokemon.add_move(move)
                
        return pokemon
        
    @staticmethod
    def create_random_pokemon(min_level=1, max_level=5):
        """创建一个随机的宝可梦"""
        import random
        pokemon_id = random.choice(list(POKEMON_DATA.keys()))
        level = random.randint(min_level, max_level)
        return PokemonFactory.create_pokemon(pokemon_id, level) 