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