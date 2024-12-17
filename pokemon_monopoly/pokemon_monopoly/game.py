import random
from .player import Player
from .battle import Battle
from .pokemon_factory import PokemonFactory
from .save_system import SaveSystem
from .event_system import EventSystem

class Cell:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.owner = None

class Game:
    def __init__(self):
        # 定义内外圈格子
        self.outer_circle = [
            # 外圈格子（24个）- 均匀分布宝可梦中心
            Cell('pokemon_center', '宝可梦中心'),  # 0
            Cell('wild_area', '野外'),
            Cell('shop', '商店'),
            Cell('wild_area', '野外'),
            Cell('teleport', '传送'),  # 4
            Cell('wild_area', '野外'),
            Cell('pokemon_center', '宝可梦中心'),  # 6
            Cell('wild_area', '野外'),
            Cell('shop', '商店'),
            Cell('wild_area', '野外'),
            Cell('gym', '道馆'),
            Cell('wild_area', '野外'),
            Cell('pokemon_center', '宝可梦中心'),  # 12
            Cell('wild_area', '野外'),
            Cell('shop', '商店'),
            Cell('wild_area', '野外'),
            Cell('special', '特殊'),
            Cell('wild_area', '野外'),
            Cell('pokemon_center', '宝可梦中心'),  # 18
            Cell('wild_area', '野外'),
            Cell('shop', '商店'),
            Cell('wild_area', '野外'),
            Cell('special', '特殊'),
            Cell('gym', '道馆')
        ]
        
        self.inner_circle = [
            # 内圈格子（16个）- 均匀分布宝可梦中心
            Cell('pokemon_center', '宝可梦中心'),  # 0
            Cell('wild_area', '野外'),
            Cell('teleport', '传送'),
            Cell('shop', '商店'),
            Cell('pokemon_center', '宝可梦中心'),  # 4
            Cell('gym', '道馆'),
            Cell('wild_area', '野外'),
            Cell('special', '特殊'),
            Cell('pokemon_center', '宝可梦中心'),  # 8
            Cell('shop', '商店'),
            Cell('wild_area', '野外'),
            Cell('gym', '道馆'),
            Cell('pokemon_center', '宝可梦中心'),  # 12
            Cell('special', '特殊'),
            Cell('wild_area', '野外'),
            Cell('shop', '商店')
        ]
        
        # 记录传送格子的位置
        self.outer_teleport_pos = 4  # 外圈传送格子的位置
        self.inner_teleport_pos = 2  # 内圈传送格子的位置
        
        # 初始化玩家（随机分配在外圈的位置）
        outer_positions = list(range(len(self.outer_circle)))
        outer_positions.remove(self.outer_teleport_pos)  # 避免初始位置在传送格子上
        random.shuffle(outer_positions)
        
        self.players = [
            Player("玩家1", starting_position=outer_positions[0], circle='outer'),
            Player("玩家2", starting_position=outer_positions[1], circle='outer')
        ]
        self.current_player = 0
        
        # 添加骰子相关属性
        self.last_roll = None
        
        # 添加事件系统
        self.event_system = EventSystem(self)

    def handle_teleport(self, player):
        """处理传送逻辑"""
        if player.circle == 'outer' and player.position == self.outer_teleport_pos:
            player.circle = 'inner'
            player.position = self.inner_teleport_pos
            return True
        elif player.circle == 'inner' and player.position == self.inner_teleport_pos:
            player.circle = 'outer'
            player.position = self.outer_teleport_pos
            return True
        return False

    def move_player(self, steps):
        """处理玩家实际移动"""
        current_player = self.players[self.current_player]
        old_position = current_player.position
        
        # 计算新位置
        if current_player.circle == 'outer':
            new_position = (old_position + steps) % len(self.outer_circle)
        else:
            new_position = (old_position + steps) % len(self.inner_circle)
        
        # 更新位置
        current_player.position = new_position
        
        # 检查是否需要传送
        was_teleported = self.handle_teleport(current_player)
        
        return {
            'old_position': old_position,
            'new_position': new_position,
            'was_teleported': was_teleported,
            'final_position': current_player.position,
            'final_circle': current_player.circle
        }

    def handle_cell_event(self, player):
        """处理当前格子事件"""
        current_cell = self.get_current_cell(player)
        return self.event_system.handle_cell_event(player, current_cell.type)

    def get_current_cell(self, player):
        """获取玩家当前所在的格子"""
        if player.circle == 'outer':
            return self.outer_circle[player.position]
        else:
            return self.inner_circle[player.position]

    def roll_dice(self):
        """只负责投骰子并返回点数"""
        result = random.randint(1, 6)
        self.last_roll = result
        return result

    def get_current_player(self):
        """获取当前玩家"""
        return self.players[self.current_player]

    def next_player(self):
        """切换到下一个玩家"""
        self.current_player = (self.current_player + 1) % len(self.players)