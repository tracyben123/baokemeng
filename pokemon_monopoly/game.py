import random

class Cell:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        self.owner = None

class Game:
    def __init__(self):
        # 初始化棋盘
        self.board = []
        self._create_board()
        
        # 初始化玩家
        self.players = []
        self.current_player = 0
        
        # 添加测试玩家
        self.add_player("玩家1", "red")
        self.add_player("玩家2", "blue")
        
        # 为测试玩家添加初始宝可梦
        for player in self.players:
            starter_pokemon = PokemonFactory.create_pokemon('pikachu', 5)
            player.add_pokemon(starter_pokemon)
        
        # 游戏状态
        self.dice_number = 0
        self.game_over = False
    
    def _create_board(self):
        # 创建20个格子的棋盘
        cell_types = ['pokemon_center', 'gym', 'shop', 'wild_area'] * 5
        random.shuffle(cell_types)
        
        for i, type in enumerate(cell_types):
            self.board.append(Cell(type, f"Cell {i}"))
    
    def roll_dice(self):
        self.dice_number = random.randint(1, 6)
        return self.dice_number
    
    def update(self):
        # 更新游戏状态
        if self.dice_number > 0:
            # 移动当前玩家
            # TODO: 实现玩家移动逻辑
            self.dice_number = 0
            
        # 检查游戏是否结束
        # TODO: 实现游戏结束条件
    
    def add_player(self, name, color):
        """添加玩家"""
        if len(self.players) < 4:
            player = Player(name, color)
            self.players.append(player)
            return True
        return False
        
    def handle_cell_event(self, player, cell):
        """处理格子事件"""
        if cell.type == 'pokemon_center':
            self._handle_pokemon_center(player)
        elif cell.type == 'gym':
            self._handle_gym(player)
        elif cell.type == 'shop':
            self._handle_shop(player)
        elif cell.type == 'wild_area':
            self._handle_wild_area(player)
            
    def _handle_pokemon_center(self, player):
        """处理宝可梦中心事件"""
        for pokemon in player.pokemon_list:
            pokemon.heal(pokemon.max_hp)
            
    def _handle_gym(self, player):
        """处理道馆事件"""
        # 创建道馆训练家的宝可梦
        gym_pokemon = [
            PokemonFactory.create_pokemon('charmander', 5),
            PokemonFactory.create_pokemon('squirtle', 5),
            PokemonFactory.create_pokemon('bulbasaur', 5)
        ]
        
        # 创建道馆训练家
        gym_trainer = Player("道馆训练家", "yellow")
        for pokemon in gym_pokemon:
            gym_trainer.add_pokemon(pokemon)
            
        # 开始战斗
        battle = self.start_battle(player, gym_trainer)
        
        return {
            'type': 'gym_battle',
            'trainer': gym_trainer,
            'battle': battle
        }
        
    def _handle_shop(self, player):
        """处理商店事件"""
        # TODO: 实现商店购买逻辑
        pass
        
    def _handle_wild_area(self, player):
        """处理野外区域事件"""
        # 随机��成一个野生宝可梦
        wild_pokemon = PokemonFactory.create_random_pokemon()
        
        # 开始战斗
        battle = self.start_battle(player, None, is_wild=True)
        battle.wild_pokemon = wild_pokemon
        
        return {
            'type': 'wild_battle',
            'pokemon': wild_pokemon,
            'battle': battle
        }
        
    def start_battle(self, player1, player2, is_wild=False):
        """开始战斗"""
        battle = Battle(player1, player2, is_wild)
        return battle
        
    def catch_pokemon(self, player, pokemon):
        """捕获宝可梦"""
        if player.items.get('pokeball', 0) > 0:
            if player.add_pokemon(pokemon):
                player.items['pokeball'] -= 1
                return True
        return False
        
    def save_game(self, filename='autosave.json'):
        """保存游戏"""
        save_system = SaveSystem()
        save_system.save_game(self, filename)
        
    def load_game(self, filename='autosave.json'):
        """加载游戏"""
        save_system = SaveSystem()
        loaded_game = save_system.load_game(filename)
        if loaded_game:
            self.__dict__.update(loaded_game.__dict__)
            return True
        return False