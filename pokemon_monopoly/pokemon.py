class Pokemon:
    def __init__(self, name, type, level=1):
        self.name = name
        self.type = type
        self.level = level
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 10
        self.moves = []
        self.experience = 0
        
    def add_move(self, move):
        """添加技能"""
        if len(self.moves) < 4:
            self.moves.append(move)
            return True
        return False
        
    def level_up(self):
        """升级"""
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 2
        self.defense += 2
        
    def take_damage(self, amount):
        """受到伤害"""
        self.hp = max(0, self.hp - amount)
        return self.hp <= 0
        
    def heal(self, amount):
        """恢复生命值"""
        self.hp = min(self.max_hp, self.hp + amount)