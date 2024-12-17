class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 0
        self.money = 1000
        self.pokemon_list = []
        self.items = {
            'pokeball': 3,
            'potion': 2,
            'evolution_stone': 0
        }
        
    def move(self, steps, board_size):
        """移动玩家位置"""
        self.position = (self.position + steps) % board_size
        return self.position
        
    def add_pokemon(self, pokemon):
        """添加宝可梦到列表"""
        if len(self.pokemon_list) < 6:
            self.pokemon_list.append(pokemon)
            return True
        return False
        
    def remove_pokemon(self, pokemon):
        """从列表中移除宝可梦"""
        if pokemon in self.pokemon_list:
            self.pokemon_list.remove(pokemon)
            return True
        return False
        
    def use_item(self, item_name):
        """使用道具"""
        if self.items.get(item_name, 0) > 0:
            self.items[item_name] -= 1
            return True
        return False