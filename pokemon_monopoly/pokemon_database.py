import random

class PokemonDatabase:
    def __init__(self):
        self.pokemon_data = {
            'pikachu': {
                'name': '皮卡丘',
                'type1': 'electric',
                'type2': None,
                'base_hp': 5,
                'skills': ['电击', '十万伏特'],
                'possible_abilities': ['静电', '避雷针'],
                'evolution': 'raichu',
                'stats': {
                    'speed': 1,
                    'attack': 0,
                    'defense': 0,
                    'sp_attack': 1,
                    'sp_defense': 0,
                    'evasion': 0
                }
            },
            'charmander': {
                'name': '小火龙',
                'type1': 'fire',
                'type2': None,
                'base_hp': 5,
                'skills': ['火花', '喷射火焰'],
                'possible_abilities': ['猛火', '太阳之力'],
                'evolution': 'charmeleon',
                'stats': {
                    'speed': 0,
                    'attack': 1,
                    'defense': 0,
                    'sp_attack': 1,
                    'sp_defense': 0,
                    'evasion': 0
                }
            },
            'squirtle': {
                'name': '杰尼龟',
                'type1': 'water',
                'type2': None,
                'base_hp': 5,
                'skills': ['水枪', '水之波动'],
                'possible_abilities': ['激流', '雨盾'],
                'evolution': 'wartortle',
                'stats': {
                    'speed': 0,
                    'attack': 0,
                    'defense': 1,
                    'sp_attack': 1,
                    'sp_defense': 0,
                    'evasion': 0
                }
            },
            'bulbasaur': {
                'name': '妙蛙种子',
                'type1': 'grass',
                'type2': 'poison',
                'base_hp': 5,
                'skills': ['藤鞭', '飞叶快刀'],
                'possible_abilities': ['茂盛', '叶绿素'],
                'evolution': 'ivysaur',
                'stats': {
                    'speed': 0,
                    'attack': 0,
                    'defense': 0,
                    'sp_attack': 1,
                    'sp_defense': 1,
                    'evasion': 0
                }
            }
        }
        
        self.skill_data = {
            '电击': {
                'effect_type': 'paralysis',
                'power': 1
            },
            '十万伏特': {
                'effect_type': 'paralysis',
                'power': 2
            },
            '火花': {
                'effect_type': 'burn',
                'power': 1
            },
            '喷射火焰': {
                'effect_type': 'burn',
                'power': 2
            },
            '水枪': {
                'effect_type': 'normal',
                'power': 1
            },
            '水之波动': {
                'effect_type': 'confusion',
                'power': 2
            },
            '藤鞭': {
                'effect_type': 'normal',
                'power': 1
            },
            '飞叶快刀': {
                'effect_type': 'critical',
                'power': 2
            }
        }
        
        # 添加属性相克关系
        self.type_chart = {
            'fire': ['grass', 'ice', 'bug', 'steel'],
            'water': ['fire', 'ground', 'rock'],
            'grass': ['water', 'ground', 'rock'],
            'electric': ['water', 'flying'],
            'ice': ['grass', 'ground', 'flying', 'dragon'],
            'fighting': ['normal', 'ice', 'rock', 'dark', 'steel'],
            'poison': ['grass', 'fairy'],
            'ground': ['fire', 'electric', 'poison', 'rock', 'steel'],
            'flying': ['grass', 'fighting', 'bug'],
            'psychic': ['fighting', 'poison'],
            'bug': ['grass', 'psychic', 'dark'],
            'rock': ['fire', 'ice', 'flying', 'bug'],
            'ghost': ['psychic', 'ghost'],
            'dragon': ['dragon'],
            'dark': ['psychic', 'ghost'],
            'steel': ['ice', 'rock', 'fairy'],
            'fairy': ['fighting', 'dragon', 'dark']
        }
        
        # 在原有宝可梦数据基础上添加进化后的宝可梦
        self.pokemon_data.update({
            'raichu': {
                'name': '雷丘',
                'type1': 'electric',
                'type2': None,
                'base_hp': 6,
                'skills': ['电击', '十万伏特', '打雷'],
                'possible_abilities': ['静电', '避雷针'],
                'evolution': None,
                'stats': {
                    'speed': 2,
                    'attack': 1,
                    'defense': 0,
                    'sp_attack': 2,
                    'sp_defense': 0,
                    'evasion': 0
                }
            },
            'charmeleon': {
                'name': '火恐龙',
                'type1': 'fire',
                'type2': None,
                'base_hp': 6,
                'skills': ['火花', '喷射火焰', '火焰旋涡'],
                'possible_abilities': ['猛火', '太阳之力'],
                'evolution': 'charizard',
                'stats': {
                    'speed': 1,
                    'attack': 1,
                    'defense': 0,
                    'sp_attack': 2,
                    'sp_defense': 0,
                    'evasion': 0
                }
            },
            'wartortle': {
                'name': '卡咪龟',
                'type1': 'water',
                'type2': None,
                'base_hp': 6,
                'skills': ['水枪', '水之波动', '急冻光线'],
                'possible_abilities': ['激流', '雨盾'],
                'evolution': 'blastoise',
                'stats': {
                    'speed': 0,
                    'attack': 0,
                    'defense': 2,
                    'sp_attack': 1,
                    'sp_defense': 1,
                    'evasion': 0
                }
            },
            'ivysaur': {
                'name': '妙蛙草',
                'type1': 'grass',
                'type2': 'poison',
                'base_hp': 6,
                'skills': ['藤鞭', '飞叶快刀', '催眠粉'],
                'possible_abilities': ['茂盛', '叶绿素'],
                'evolution': 'venusaur',
                'stats': {
                    'speed': 0,
                    'attack': 1,
                    'defense': 1,
                    'sp_attack': 1,
                    'sp_defense': 1,
                    'evasion': 0
                }
            }
        })
        
        # 添加新技能
        self.skill_data.update({
            '打雷': {
                'effect_type': 'paralysis',
                'power': 3
            },
            '火焰旋涡': {
                'effect_type': 'burn',
                'power': 3
            },
            '急冻光线': {
                'effect_type': 'frozen',
                'power': 2
            },
            '催眠粉': {
                'effect_type': 'sleep',
                'power': 2
            }
        })
        
    def create_pokemon(self, pokemon_id):
        if pokemon_id not in self.pokemon_data:
            raise ValueError(f"未知的宝可梦ID: {pokemon_id}")
            
        data = self.pokemon_data[pokemon_id]
        pokemon = Pokemon(
            name=data['name'],
            type1=data['type1'],
            type2=data['type2'],
            hp=data['base_hp']
        )
        
        # 设置技能
        for skill_name in data['skills']:
            skill_data = self.skill_data[skill_name]
            pokemon.skills.append(Skill(
                name=skill_name,
                effect_type=skill_data['effect_type'],
                power=skill_data['power']
            ))
            
        # 设置属性
        pokemon.stats = data['stats'].copy()
        
        # 设置进化信息
        if data['evolution']:
            pokemon.evolution = lambda p: self.create_pokemon(data['evolution'])
            
        return pokemon
        
    def generate_wild_pokemon(self):
        # 随机生成野生宝可梦
        pokemon_id = random.choice(list(self.pokemon_data.keys()))
        return self.create_pokemon(pokemon_id)
        
    def generate_league_pokemon(self):
        # 生成联盟对战的宝可梦队伍
        pokemon_ids = random.sample(list(self.pokemon_data.keys()), 3)
        return [self.create_pokemon(pid) for pid in pokemon_ids] 