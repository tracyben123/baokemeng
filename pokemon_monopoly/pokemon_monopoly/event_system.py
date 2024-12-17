from .pokemon_factory import PokemonFactory

class EventSystem:
    def __init__(self, game):
        self.game = game
        self.pokemon_factory = PokemonFactory()
    
    def handle_cell_event(self, player, cell_type):
        """处理格子事件"""
        handlers = {
            'wild_area': self._handle_wild_area,
            'pokemon_center': self._handle_pokemon_center,
            'shop': self._handle_shop,
            'gym': self._handle_gym,
            'special': self._handle_special_event
        }
        
        if cell_type in handlers:
            return handlers[cell_type](player)
        return None
    
    def _handle_wild_area(self, player):
        """处理野外区域事件"""
        # 获取玩家最高等级的宝可梦
        max_level = max(p.level for p in player.pokemon_list)
        # 生成野生宝可梦
        wild_pokemon = self.pokemon_factory.create_wild_pokemon(max_level)
        
        return {
            'type': 'battle',
            'battle_type': 'wild',
            'enemy': wild_pokemon,
            'can_catch': True
        }
    
    def _handle_pokemon_center(self, player):
        """处理宝可梦中心事件"""
        return {
            'type': 'pokemon_center',
            'message': '欢迎来到宝可梦中心！'
        }
    
    def _handle_shop(self, player):
        """处理商店事件"""
        shop_items = [
            {
                'name': '精灵球',
                'id': 'pokeball',
                'price': 200,
                'description': '用于捕捉野生宝可梦'
            },
            {
                'name': '伤药',
                'id': 'potion',
                'price': 300,
                'description': '恢复宝可梦50点HP'
            },
            {
                'name': '进化石',
                'id': 'evolution_stone',
                'price': 1000,
                'description': '让特定宝可梦进化'
            }
        ]
        
        return {
            'type': 'shop',
            'items': shop_items
        }
    
    def _handle_gym(self, player):
        """处理道馆事件"""
        # 创建道馆训练师的宝可梦
        max_level = max(p.level for p in player.pokemon_list)
        gym_pokemon = self.pokemon_factory.create_gym_pokemon(max_level)
        
        return {
            'type': 'battle',
            'battle_type': 'gym',
            'enemy': gym_pokemon,
            'reward': {
                'money': 1000,
                'item': {
                    'id': 'badge',
                    'name': '道馆徽章'
                }
            }
        }
    
    def _handle_special_event(self, player):
        """处理特殊事件"""
        # 随机选择一个特殊事件
        events = [
            {
                'type': 'find_item',
                'item': {'id': 'rare_candy', 'name': '神奇糖果'},
                'message': '你发现了一个神奇糖果！'
            },
            {
                'type': 'money',
                'amount': 500,
                'message': '你捡到了500元！'
            },
            {
                'type': 'pokemon_egg',
                'pokemon': self.pokemon_factory.create_pokemon(level=1),
                'message': '你发现了一个宝可梦蛋！'
            }
        ]
        
        import random
        event = random.choice(events)
        
        # 处理事件效果
        if event['type'] == 'find_item':
            player.add_item(event['item']['id'])
        elif event['type'] == 'money':
            player.add_money(event['amount'])
        elif event['type'] == 'pokemon_egg':
            player.add_pokemon(event['pokemon'])
        
        return event 