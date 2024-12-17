class Skill:
    def __init__(self, name, effect_type, power=1):
        self.name = name
        self.effect_type = effect_type
        self.power = power
        
    def can_trigger(self):
        # 判断技能是否可以触发（骰子为6）
        return True
        
    def apply_effect(self, target):
        if self.effect_type == 'paralysis':
            target.apply_status('paralyzed')
        elif self.effect_type == 'poison':
            target.apply_status('poisoned')
        elif self.effect_type == 'burn':
            target.apply_status('burned')
        elif self.effect_type == 'confusion':
            target.apply_status('confused')
        # 添加更多技能效果 