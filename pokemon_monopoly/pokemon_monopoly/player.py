from .pokemon import Pokemon  # 添加这行导入

class Player:
    MAX_POKEMON = 5  # 设置宝可梦上限为5只

    def __init__(self, name, starting_position=0, circle='outer'):
        self.name = name
        self.position = starting_position
        self.circle = circle  # 新增：记录玩家在哪个圈
        self.money = 1000
        self.pokemon_list = []  # 每个玩家独立的宝可梦列表
        self.items = {
            'pokeball': 5,    # 初始道具
            'potion': 3,
            'evolution_stone': 1
        }
        
        # 为每个玩家分配不同的初始宝可梦
        if name == "玩家1":
            from .pokemon import Pokemon
            starter = Pokemon("皮卡丘", "pikachu", level=5)
            self.add_pokemon(starter)
        elif name == "玩家2":
            from .pokemon import Pokemon
            starter = Pokemon("小火龙", "charmander", level=5)
            self.add_pokemon(starter)

    def move(self, steps, board_size):
        """移动玩家"""
        self.position = (self.position + steps) % board_size

    def add_pokemon(self, pokemon):
        """添加宝可梦到队伍"""
        if len(self.pokemon_list) < self.MAX_POKEMON:
            self.pokemon_list.append(pokemon)
            return True
        return False

    def remove_pokemon(self, index):
        """从队伍中移除宝可梦"""
        if 0 <= index < len(self.pokemon_list):
            return self.pokemon_list.pop(index)
        return None

    def has_item(self, item_name):
        """检查是否有某个道具"""
        return self.items.get(item_name, 0) > 0

    def use_item(self, item_name):
        """使用道具"""
        if self.has_item(item_name):
            self.items[item_name] -= 1
            return True
        return False

    def add_item(self, item_name, count=1):
        """添加道具"""
        self.items[item_name] = self.items.get(item_name, 0) + count

    def add_money(self, amount):
        """增加金钱"""
        self.money += amount

    def spend_money(self, amount):
        """花费金钱"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False 