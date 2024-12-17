from .data.pokemon_data import POKEMON_DATA, TYPE_CHART
import random

class Pokemon:
    def __init__(self, name, species, level=1):
        self.name = name
        self.species = species
        self.type = POKEMON_DATA[species]['type']
        self.level = level
        
        # 初始化基础属性
        self.stats = {
            'hp': 50 + level * 5,
            'attack': 10 + level * 2,
            'defense': 10 + level * 2,
            'speed': 10 + level * 2
        }
        
        # 初始化当前HP
        self.current_hp = self.stats['hp']
        
        # 初始化技能列表
        self.moves = [
            {
                'name': '撞击',
                'power': 40,
                'pp': 35,
                'type': 'normal'
            },
            {
                'name': '电光一闪',
                'power': 30,
                'pp': 30,
                'type': 'normal'
            },
            {
                'name': '十万伏特',
                'power': 15,
                'pp': 15,
                'type': 'electric'
            }
        ]
        
        # 初始化技能PP
        self.current_pp = {}
        for move in self.moves:
            self.current_pp[move['name']] = move['pp']
    
    def _calculate_stats(self):
        """根据等级计算实际属性值"""
        stats = {}
        base_stats = self.data['base_stats']
        for stat, base in base_stats.items():
            # 简化的属性计算公式
            stats[stat] = int(base * (1 + self.level/50))
        return stats
    
    def use_move(self, move_index, target):
        """使用技能攻击目标"""
        move = self.moves[move_index]
        
        # 检查PP
        if self.current_pp[move['name']] <= 0:
            return {
                'success': False,
                'message': f'{self.name}的{move["name"]}没有PP了！'
            }
        
        # 消耗PP
        self.current_pp[move['name']] -= 1
        
        # 计算伤害
        # 基础伤害 = (攻击方等级 × 0.4 + 2) × 技能威力 × (攻击方攻击力 / 防御方防御力) × 0.02
        base_damage = (self.level * 0.4 + 2) * move['power'] * (self.stats['attack'] / target.stats['defense']) * 0.02
        
        # 属性相克修正
        type_modifier = self._get_type_effectiveness(move['type'], target.type)
        
        # 随机浮动 (0.85-1.15)
        random_factor = 0.85 + random.random() * 0.3
        
        # 暴击判定 (10%概率，1.5倍伤害)
        is_critical = random.random() < 0.1
        critical_mod = 1.5 if is_critical else 1.0
        
        # 最终伤害
        final_damage = int(base_damage * type_modifier * random_factor * critical_mod)
        
        # 确保最小伤害为1
        final_damage = max(1, final_damage)
        
        # 造成伤害
        target.current_hp = max(0, target.current_hp - final_damage)
        
        # 生成战斗消息
        message = f'{self.name}使用了{move["name"]}！'
        if type_modifier > 1:
            message += '效果拔群！'
        elif type_modifier < 1:
            message += '效果不太好...'
        if is_critical:
            message += '会心一击！'
        message += f'\n造成了{final_damage}点伤害！'
        
        return {
            'success': True,
            'damage': final_damage,
            'message': message,
            'is_critical': is_critical,
            'type_effectiveness': type_modifier
        }
    
    def _get_type_effectiveness(self, move_type, target_type):
        """计算属性相克倍率"""
        from .data.pokemon_data import TYPE_CHART
        
        # 如果没有属性相克数据，返回1.0
        if move_type not in TYPE_CHART or target_type not in TYPE_CHART:
            return 1.0
        
        effectiveness = 1.0
        
        # 检查是否免疫
        if target_type in TYPE_CHART[move_type].get('immune', []):
            return 0.0
        
        # 检查是否效果拔群
        if target_type in TYPE_CHART[move_type].get('super_effective', []):
            effectiveness *= 1.5
        
        # 检查是否效果不好
        if target_type in TYPE_CHART[move_type].get('not_effective', []):
            effectiveness *= 0.5
        
        return effectiveness
    
    def take_damage(self, amount):
        """受到伤害"""
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp == 0
    
    def heal(self, amount):
        """恢复生命值"""
        self.current_hp = min(self.stats['hp'], self.current_hp + amount)
    
    def gain_exp(self, amount):
        """获得经验值"""
        self.exp += amount
        if self.exp >= self.exp_needed:
            return self.level_up()
        return False
    
    def level_up(self):
        """升级"""
        self.level += 1
        old_stats = self.stats.copy()
        self.stats = self._calculate_stats()
        
        # 检查是否可以进化
        can_evolve = False
        if 'evolution' in self.data:
            if self.level >= self.data['evolution']['level']:
                can_evolve = True
        
        return {
            'level_up': True,
            'old_stats': old_stats,
            'new_stats': self.stats,
            'can_evolve': can_evolve
        } 