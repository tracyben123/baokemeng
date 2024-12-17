# 预定义的宝可梦数据
POKEMON_DATA = {
    'pikachu': {
        'name': '皮卡丘',
        'type': 'electric',
        'base_stats': {
            'hp': 35,
            'attack': 55,
            'defense': 40
        },
        'moves': ['thunder_shock', 'quick_attack']
    },
    'charmander': {
        'name': '小火龙',
        'type': 'fire',
        'base_stats': {
            'hp': 39,
            'attack': 52,
            'defense': 43
        },
        'moves': ['ember', 'scratch']
    },
    'squirtle': {
        'name': '杰尼龟',
        'type': 'water',
        'base_stats': {
            'hp': 44,
            'attack': 48,
            'defense': 65
        },
        'moves': ['water_gun', 'tackle']
    },
    'bulbasaur': {
        'name': '妙蛙种子',
        'type': 'grass',
        'base_stats': {
            'hp': 45,
            'attack': 49,
            'defense': 49
        },
        'moves': ['vine_whip', 'tackle']
    }
}

# 预定义的技能数据
MOVE_DATA = {
    'thunder_shock': {
        'name': '电击',
        'type': 'electric',
        'power': 40,
        'accuracy': 100
    },
    'quick_attack': {
        'name': '电光一闪',
        'type': 'normal',
        'power': 40,
        'accuracy': 100
    },
    'scratch': {
        'name': '抓',
        'type': 'normal',
        'power': 40,
        'accuracy': 100
    },
    'ember': {
        'name': '火花',
        'type': 'fire',
        'power': 40,
        'accuracy': 100
    },
    'water_gun': {
        'name': '水枪',
        'type': 'water',
        'power': 40,
        'accuracy': 100
    },
    'vine_whip': {
        'name': '藤鞭',
        'type': 'grass',
        'power': 40,
        'accuracy': 100
    },
    'tackle': {
        'name': '撞击',
        'type': 'normal',
        'power': 35,
        'accuracy': 95
    }
} 