from enum import Enum, auto

class TurnState(Enum):
    READY = auto()      # 回合开始，等待投骰子
    ROLLING = auto()    # 正在投骰子
    MOVING = auto()     # 正在移动
    EVENT = auto()      # 处理格子事件
    FINISHED = auto()   # 回合结束

class EventType(Enum):
    BATTLE = auto()         # 战斗
    SHOP = auto()          # 商店
    POKEMON_CENTER = auto() # 宝可梦中心
    TELEPORT = auto()      # 传送
    SPECIAL = auto()       # 特殊事件 