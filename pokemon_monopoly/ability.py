class Ability:
    def __init__(self, name, effect_type, duration=5):
        self.name = name
        self.effect_type = effect_type
        self.duration = duration  # 特性持续的对战次数
        self.is_active = False
        self.battles_remaining = 0
        
    def activate(self):
        self.is_active = True
        self.battles_remaining = self.duration
        
    def deactivate(self):
        self.is_active = False
        self.battles_remaining = 0
        
    def use_battle(self):
        if self.is_active:
            self.battles_remaining -= 1
            if self.battles_remaining <= 0:
                self.deactivate()
                
    def apply_effect(self, pokemon, battle_context):
        if not self.is_active:
            return
            
        if self.effect_type == 'high_critical':
            # 提高技能触发几率
            if battle_context.roll == 5:
                battle_context.trigger_skill = True
        elif self.effect_type == 'skill_immune':
            # 技能免疫
            if battle_context.is_skill and battle_context.defense_roll in [5, 6]:
                battle_context.damage = 0
        elif self.effect_type == 'skill_boost':
            # 提高技能伤害
            if battle_context.is_skill:
                battle_context.damage *= 2 