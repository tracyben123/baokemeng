import random

class Battle:
    def __init__(self, player1, player2, is_wild=False):
        self.player1 = player1
        self.player2 = player2
        self.is_wild = is_wild
        self.current_turn = 0
        self.active_pokemon1 = player1.pokemon_list[0] if player1.pokemon_list else None
        self.active_pokemon2 = player2.pokemon_list[0] if player2.pokemon_list else None
        
    def execute_turn(self, move_index):
        """执行一个回合的战斗"""
        if not self.active_pokemon1 or not self.active_pokemon2:
            return False
            
        # 获取选择的技能
        if move_index < len(self.active_pokemon1.moves):
            move = self.active_pokemon1.moves[move_index]
            
            # 计算伤害
            damage = self._calculate_damage(self.active_pokemon1, self.active_pokemon2, move)
            
            # 造成伤害
            is_fainted = self.active_pokemon2.take_damage(damage)
            
            # 如果宝可梦失败，切换到下一个
            if is_fainted:
                self._switch_pokemon(self.player2)
                
            return True
        return False
        
    def _calculate_damage(self, attacker, defender, move):
        """计算伤害值"""
        base_damage = attacker.attack - defender.defense // 2
        type_bonus = self._get_type_bonus(move.type, defender.type)
        return max(1, int(base_damage * type_bonus))
        
    def _get_type_bonus(self, attack_type, defend_type):
        """获取属性克制关系加成"""
        type_chart = {
            'fire': {'grass': 2.0, 'water': 0.5},
            'water': {'fire': 2.0, 'grass': 0.5},
            'grass': {'water': 2.0, 'fire': 0.5}
        }
        return type_chart.get(attack_type, {}).get(defend_type, 1.0)
        
    def _switch_pokemon(self, player):
        """切换到下一个可用的宝可梦"""
        for pokemon in player.pokemon_list:
            if pokemon.hp > 0:
                if player == self.player1:
                    self.active_pokemon1 = pokemon
                else:
                    self.active_pokemon2 = pokemon
                return True
        return False