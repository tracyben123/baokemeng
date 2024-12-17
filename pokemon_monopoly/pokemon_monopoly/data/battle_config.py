# 战斗系统配置
BATTLE_CONFIG = {
    # 捕捉相关
    'catch_rates': {
        'base_rate': 0.3,        # 基础捕获率
        'hp_bonus': 0.4,         # HP越低捕获率越高，最多+40%
        'status_bonus': 0.2,     # 异常状态加成20%
        'ball_rates': {
            'pokeball': 1.0,     # 普通精灵球
            'greatball': 1.5,    # 高级球
            'ultraball': 2.0,    # 超级球
            'masterball': 100.0  # 大师球
        }
    },
    
    # 战斗动画配置
    'animations': {
        'attack': {
            'duration': 800,     # 攻击动画持续时间(ms)
            'frames': 6          # 动画帧数
        },
        'damage': {
            'duration': 500,
            'frames': 4
        },
        'catch': {
            'duration': 2000,
            'frames': 8
        },
        'evolution': {
            'duration': 3000,
            'frames': 10
        }
    },
    
    # 战斗音效
    'sounds': {
        'attack': 'attack.wav',
        'hit': 'hit.wav',
        'critical': 'critical.wav',
        'catch_start': 'catch_start.wav',
        'catch_shake': 'catch_shake.wav',
        'catch_success': 'catch_success.wav',
        'catch_fail': 'catch_fail.wav',
        'evolution_start': 'evolution_start.wav',
        'evolution_complete': 'evolution_complete.wav'
    },
    
    # 战斗背景音乐
    'music': {
        'wild_battle': 'wild_battle.mp3',
        'trainer_battle': 'trainer_battle.mp3',
        'gym_battle': 'gym_battle.mp3',
        'victory': 'victory.mp3'
    }
} 