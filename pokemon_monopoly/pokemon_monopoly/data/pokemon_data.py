# 宝可梦基础数据
POKEMON_DATA = {
    'pikachu': {
        'name': '皮卡丘',
        'type': 'electric',
        'base_stats': {
            'hp': 60,
            'attack': 55,
            'defense': 50,
            'speed': 90
        },
        'moves': [
            {
                'name': '电击',
                'type': 'electric',
                'power': 40,
                'accuracy': 100,
                'pp': 30
            },
            {
                'name': '电光一闪',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 30
            },
            {
                'name': '十万伏特',
                'type': 'electric',
                'power': 90,
                'accuracy': 100,
                'pp': 15
            }
        ],
        'evolution': {
            'level': 30,
            'to': 'raichu'
        }
    },
    'charmander': {
        'name': '小火龙',
        'type': 'fire',
        'base_stats': {
            'hp': 39,
            'attack': 52,
            'defense': 43,
            'speed': 65
        },
        'moves': [
            {
                'name': '火花',
                'type': 'fire',
                'power': 40,
                'accuracy': 100,
                'pp': 25
            },
            {
                'name': '抓',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 35
            },
            {
                'name': '火焰放射',
                'type': 'fire',
                'power': 90,
                'accuracy': 100,
                'pp': 15
            }
        ],
        'evolution': {
            'level': 16,
            'to': 'charmeleon'
        }
    },
    'squirtle': {
        'name': '杰尼龟',
        'type': 'water',
        'base_stats': {
            'hp': 44,
            'attack': 48,
            'defense': 65,
            'speed': 43
        },
        'moves': [
            {
                'name': '水枪',
                'type': 'water',
                'power': 40,
                'accuracy': 100,
                'pp': 25
            },
            {
                'name': '撞击',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 35
            },
            {
                'name': '���炮',
                'type': 'water',
                'power': 110,
                'accuracy': 80,
                'pp': 5
            }
        ],
        'evolution': {
            'level': 16,
            'to': 'wartortle'
        }
    },
    'bulbasaur': {  # 妙蛙种子
        'name': '妙蛙种子',
        'type': 'grass',
        'base_stats': {
            'hp': 45,
            'attack': 49,
            'defense': 49,
            'speed': 45
        },
        'moves': [
            {
                'name': '撞击',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 35
            },
            {
                'name': '藤鞭',
                'type': 'grass',
                'power': 45,
                'accuracy': 100,
                'pp': 25
            },
            {
                'name': '毒粉',
                'type': 'poison',
                'power': 0,
                'accuracy': 75,
                'pp': 35
            }
        ],
        'evolution': {
            'level': 16,
            'to': 'ivysaur'
        }
    },
    'eevee': {  # 伊布
        'name': '伊布',
        'type': 'normal',
        'base_stats': {
            'hp': 55,
            'attack': 55,
            'defense': 50,
            'speed': 55
        },
        'moves': [
            {
                'name': '抓',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 35
            },
            {
                'name': '电光一闪',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 30
            },
            {
                'name': '撞击',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 30
            }
        ],
        'evolution': {
            'level': 16,
            'to': 'vaporeon'
        }
    },
    'meowth': {  # 喵喵
        'name': '喵喵',
        'type': 'normal',
        'base_stats': {
            'hp': 40,
            'attack': 45,
            'defense': 35,
            'speed': 90
        },
        'moves': [
            {
                'name': '抓',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 35
            },
            {
                'name': '电光一闪',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 30
            },
            {
                'name': '撞击',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 30
            }
        ],
        'evolution': {
            'level': 16,
            'to': 'persian'
        }
    },
    'psyduck': {  # 可达鸭
        'name': '可达鸭',
        'type': 'water',
        'base_stats': {
            'hp': 50,
            'attack': 52,
            'defense': 48,
            'speed': 55
        },
        'moves': [
            {
                'name': '水枪',
                'type': 'water',
                'power': 40,
                'accuracy': 100,
                'pp': 25
            },
            {
                'name': '撞击',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 35
            },
            {
                'name': '水炮',
                'type': 'water',
                'power': 110,
                'accuracy': 80,
                'pp': 5
            }
        ],
        'evolution': {
            'level': 16,
            'to': 'golduck'
        }
    },
    'growlithe': {  # 卡蒂狗
        'name': '卡蒂狗',
        'type': 'fire',
        'base_stats': {
            'hp': 60,
            'attack': 80,
            'defense': 50,
            'speed': 50
        },
        'moves': [
            {
                'name': '火花',
                'type': 'fire',
                'power': 40,
                'accuracy': 100,
                'pp': 25
            },
            {
                'name': '撞击',
                'type': 'normal',
                'power': 40,
                'accuracy': 100,
                'pp': 35
            },
            {
                'name': '火焰放射',
                'type': 'fire',
                'power': 90,
                'accuracy': 100,
                'pp': 15
            }
        ],
        'evolution': {
            'level': 16,
            'to': 'growlithe'
        }
    }
}

# 属性相克关系
TYPE_CHART = {
    'normal': {  # 一般
        'super_effective': [],  # 没有双倍效果
        'not_effective': ['rock', 'steel'],  # 对岩石和钢属性效果减半
        'immune': ['ghost']  # 对幽灵免疫
    },
    'fire': {  # 火
        'super_effective': ['grass', 'ice', 'bug', 'steel'],  # 对草、冰、虫、钢双倍
        'not_effective': ['fire', 'water', 'rock', 'dragon'],  # 对火、水、岩石、龙减半
        'immune': []
    },
    'water': {  # 水
        'super_effective': ['fire', 'ground', 'rock'],  # 对火、地面、岩石双倍
        'not_effective': ['water', 'grass', 'dragon'],  # 对水、草、龙减半
        'immune': []
    },
    'electric': {  # 电
        'super_effective': ['water', 'flying'],  # 对水、飞行双倍
        'not_effective': ['electric', 'grass', 'dragon'],  # 对电、草、龙减半
        'immune': ['ground']  # 对地面免疫
    },
    'grass': {  # 草
        'super_effective': ['water', 'ground', 'rock'],  # 对水、地面、岩石双倍
        'not_effective': ['fire', 'grass', 'poison', 'flying', 'bug', 'dragon', 'steel'],  # 效果减半
        'immune': []
    },
    'ice': {  # 冰
        'super_effective': ['grass', 'ground', 'flying', 'dragon'],  # 对草、地面、飞行、龙双倍
        'not_effective': ['fire', 'water', 'ice', 'steel'],  # 对火、水、冰、钢减半
        'immune': []
    },
    'fighting': {  # 格斗
        'super_effective': ['normal', 'ice', 'rock', 'dark', 'steel'],  # 效果双倍
        'not_effective': ['poison', 'flying', 'psychic', 'bug', 'fairy'],  # 效果减半
        'immune': ['ghost']  # 对幽灵免疫
    },
    'poison': {  # 毒
        'super_effective': ['grass', 'fairy'],  # 对草、妖精双倍
        'not_effective': ['poison', 'ground', 'rock', 'ghost'],  # 效果减半
        'immune': ['steel']  # 对钢免疫
    },
    'ground': {  # 地面
        'super_effective': ['fire', 'electric', 'poison', 'rock', 'steel'],  # 效果双倍
        'not_effective': ['grass', 'bug'],  # 效果减半
        'immune': ['flying']  # 对飞行免疫
    },
    'flying': {  # 飞行
        'super_effective': ['grass', 'fighting', 'bug'],  # 效果双倍
        'not_effective': ['electric', 'rock', 'steel'],  # 效果减半
        'immune': []
    },
    'psychic': {  # 超能力
        'super_effective': ['fighting', 'poison'],  # 效果双倍
        'not_effective': ['psychic', 'steel'],  # 效果减半
        'immune': ['dark']  # 对恶免疫
    },
    'bug': {  # 虫
        'super_effective': ['grass', 'psychic', 'dark'],  # 效果双倍
        'not_effective': ['fire', 'fighting', 'poison', 'flying', 'ghost', 'steel', 'fairy'],  # 效果减半
        'immune': []
    },
    'rock': {  # 岩石
        'super_effective': ['fire', 'ice', 'flying', 'bug'],  # 效果双倍
        'not_effective': ['fighting', 'ground', 'steel'],  # 效果减半
        'immune': []
    },
    'ghost': {  # 幽灵
        'super_effective': ['psychic', 'ghost'],  # 效果双倍
        'not_effective': ['dark'],  # 效果减半
        'immune': ['normal']  # 对一般免疫
    },
    'dragon': {  # 龙
        'super_effective': ['dragon'],  # 对龙双倍
        'not_effective': ['steel'],  # 对钢减半
        'immune': ['fairy']  # 对妖精免疫
    },
    'dark': {  # 恶
        'super_effective': ['psychic', 'ghost'],  # 效果双倍
        'not_effective': ['fighting', 'dark', 'fairy'],  # 效果减半
        'immune': []
    },
    'steel': {  # 钢
        'super_effective': ['ice', 'rock', 'fairy'],  # 效果双倍
        'not_effective': ['fire', 'water', 'electric', 'steel'],  # 效果减半
        'immune': []
    },
    'fairy': {  # 妖精
        'super_effective': ['fighting', 'dragon', 'dark'],  # 效果双倍
        'not_effective': ['fire', 'poison', 'steel'],  # 效果减半
        'immune': []
    }
} 