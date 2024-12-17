class Move:
    def __init__(self, name, type, power, accuracy):
        self.name = name
        self.type = type
        self.power = power
        self.accuracy = accuracy
        self.pp = 10  # 技能使用次数
        
    def can_use(self):
        return self.pp > 0
        
    def use(self):
        if self.can_use():
            self.pp -= 1
            return True
        return False
        
    def restore(self):
        self.pp = 10

# 预定义一些基础技能
BASIC_MOVES = {
    'tackle': Move('撞击', 'normal', 40, 100),
    'ember': Move('火花', 'fire', 40, 100),
    'water_gun': Move('水枪', 'water', 40, 100),
    'vine_whip': Move('藤鞭', 'grass', 40, 100)
} 