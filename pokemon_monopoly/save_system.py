import json
import os

class SaveSystem:
    def __init__(self, save_dir='saves'):
        self.save_dir = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
    def save_game(self, game, filename):
        """保存游戏状态"""
        save_data = {
            'players': [self._serialize_player(p) for p in game.players],
            'current_player': game.current_player,
            'board': [self._serialize_cell(c) for c in game.board]
        }
        
        filepath = os.path.join(self.save_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)
            
    def load_game(self, filename):
        """加载游戏状态"""
        filepath = os.path.join(self.save_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
                
            game = Game()  # 创建新游戏实例
            game.players = [self._deserialize_player(p) for p in save_data['players']]
            game.current_player = save_data['current_player']
            game.board = [self._deserialize_cell(c) for c in save_data['board']]
            
            return game
        return None
        
    def _serialize_player(self, player):
        """序列化玩家数据"""
        return {
            'name': player.name,
            'color': player.color,
            'position': player.position,
            'money': player.money,
            'pokemon_list': [self._serialize_pokemon(p) for p in player.pokemon_list],
            'items': player.items
        }
        
    def _serialize_pokemon(self, pokemon):
        """序列化宝可梦数据"""
        return {
            'name': pokemon.name,
            'type': pokemon.type,
            'level': pokemon.level,
            'hp': pokemon.hp,
            'max_hp': pokemon.max_hp,
            'attack': pokemon.attack,
            'defense': pokemon.defense,
            'moves': [m.__dict__ for m in pokemon.moves],
            'experience': pokemon.experience
        } 