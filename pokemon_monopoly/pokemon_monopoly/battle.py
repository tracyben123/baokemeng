from .data.battle_config import BATTLE_CONFIG
import random

class Battle:
    def __init__(self, game, player_pokemon, enemy_pokemon):
        self.game = game
        self.player = self.game.get_current_player()  # 保存当前玩家的引用
        self.player_pokemon = player_pokemon
        self.enemy_pokemon = enemy_pokemon
        self.state = 'active'
        self.messages = []
        self.can_catch = True  # 是否可以捕捉
        self.turn = 0
        self.can_escape = True  # 是否可以逃跑
        self.escape_attempts = 0
        self.catch_attempts = 0  # 记录捕捉尝试次数
        
        # 动画相关
        self.current_animation = None
        self.animation_start_time = 0
    
    def try_catch_pokemon(self):
        """尝试捕捉宝可梦"""
        if not self.can_catch:
            return {
                'success': False,
                'message': '这只宝可梦无法捕捉！'
            }
        
        # 检查是否有精灵球
        if self.player.items.get('pokeball', 0) <= 0:
            return {
                'success': False,
                'message': '没有精灵球了！'
            }
        
        # 消耗一个精灵球
        self.player.items['pokeball'] -= 1
        
        # 计算捕获率
        hp_ratio = self.enemy_pokemon.current_hp / self.enemy_pokemon.stats['hp']
        base_rate = 0.3  # 基础捕获率
        hp_bonus = 0.4 * (1 - hp_ratio)  # HP越低加成越高，��多+40%
        
        # 最终捕获率
        catch_rate = min(0.9, base_rate + hp_bonus)  # 最高90%的捕获率
        
        # 捕获判定
        success = random.random() < catch_rate
        
        if success:
            return {
                'success': True,
                'message': '捕获成功！'
            }
        else:
            # 失败后有概率逃跑
            escape_chance = 0.3 + self.catch_attempts * 0.1  # 每次失败增加10%逃跑几率
            self.catch_attempts += 1
            
            if random.random() < escape_chance:
                return {
                    'type': 'pokemon_escaped',
                    'message': f'野生的{self.enemy_pokemon.name}逃跑了！'
                }
            else:
                return {
                    'success': False,
                    'message': '差一点就抓到了！'
                }
    
    def check_evolution(self):
        """检查是否可以进化"""
        if not hasattr(self.player_pokemon, 'evolution'):
            return None
            
        if (self.player_pokemon.level >= self.player_pokemon.evolution['level']):
            return {
                'type': 'evolution',
                'pokemon': self.player_pokemon,
                'to': self.player_pokemon.evolution['to'],
                'animation': 'evolution'
            }
        return None
    
    def execute_turn(self, action):
        """执行一个回合
        action: 可以是技能索引(0,1,2,3)，'catch'表示尝试捕捉，'run'表示逃跑
        """
        self.turn += 1
        
        # 处理逃跑
        if action == 'run':
            escape_result = self._try_escape()
            if escape_result['success']:
                return {
                    'type': 'battle_escaped',
                    'messages': self.messages
                }
            else:
                self.messages.append(escape_result['message'])
        # 处理捕捉
        elif action == 'catch':
            return self.try_catch_pokemon()
        # 处理普通攻击
        else:
            # 玩家行动
            player_result = self.player_pokemon.use_move(action, self.enemy_pokemon)
            self.messages.append(player_result['message'])
            
            # 检查敌方是否失败
            if self.enemy_pokemon.current_hp == 0:
                exp_gained = self.enemy_pokemon.level * 50  # 简化的经验值计算
                level_up_result = self.player_pokemon.gain_exp(exp_gained)
                
                result = {
                    'type': 'battle_won',
                    'exp_gained': exp_gained,
                    'level_up': level_up_result if level_up_result else None,
                    'messages': self.messages
                }
                
                # 检查是否可以进化
                evolution = self.check_evolution()
                if evolution:
                    result['evolution'] = evolution
                
                return result
            
            # 敌方行动
            enemy_move_index = self._get_enemy_move()
            enemy_result = self.enemy_pokemon.use_move(enemy_move_index, self.player_pokemon)
            self.messages.append(enemy_result['message'])
            
            # 检查玩家是否失败
            if self.player_pokemon.current_hp == 0:
                return {
                    'type': 'battle_lost',
                    'messages': self.messages
                }
            
            # 战斗继续
            return {
                'type': 'battle_continue',
                'messages': self.messages
            }
    
    def _try_escape(self):
        """尝试逃跑
        逃跑成功率 = 基础成功率(50%) + 尝试次数加成(每次+10%) + 速度差值加成
        """
        if not self.can_escape:
            return {
                'success': False,
                'message': '这场战��无法逃跑！'
            }
        
        self.escape_attempts += 1
        base_chance = 0.5  # 基础50%成功率
        attempt_bonus = min(0.3, self.escape_attempts * 0.1)  # 每次尝试+10%，最多+30%
        
        # 速度差值加成：我方速度每比对方快10点，成功率+5%
        speed_diff = self.player_pokemon.stats['speed'] - self.enemy_pokemon.stats['speed']
        speed_bonus = max(0, min(0.2, speed_diff / 200))  # 最多+20%
        
        escape_chance = base_chance + attempt_bonus + speed_bonus
        
        if random.random() < escape_chance:
            return {
                'success': True,
                'message': f'{self.player_pokemon.name}成功逃跑了！'
            }
        else:
            return {
                'success': False,
                'message': f'{self.player_pokemon.name}没能逃跑！'
            }
    
    def _get_enemy_move(self):
        """获取敌方的行动（简单AI）"""
        available_moves = [
            i for i, move in enumerate(self.enemy_pokemon.moves)
            if self.enemy_pokemon.current_pp[move['name']] > 0
        ]
        
        if not available_moves:
            # 如果没有PP了，只能挣扎
            return {
                'success': False,
                'message': f'{self.enemy_pokemon.name}的PP已经用完了！'
            }
        
        # 简单的AI策略：
        # 1. 如果HP低于20%，优先使用威力较低的技能
        # 2. 如果HP高于50%，优先使用威力较高的技能
        # 3. 其他情况随机选择
        hp_ratio = self.enemy_pokemon.current_hp / self.enemy_pokemon.stats['hp']
        
        if hp_ratio < 0.2:
            # 选择威力最低的技能
            return min(available_moves, 
                      key=lambda i: self.enemy_pokemon.moves[i]['power'])
        elif hp_ratio > 0.5:
            # 选择威力最高的技能
            return max(available_moves, 
                      key=lambda i: self.enemy_pokemon.moves[i]['power'])
        else:
            return random.choice(available_moves)