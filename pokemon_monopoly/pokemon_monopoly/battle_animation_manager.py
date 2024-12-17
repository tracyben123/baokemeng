import pygame
from .data.battle_config import BATTLE_CONFIG

class BattleAnimationManager:
    def __init__(self):
        self.animations = {}
        self.current_animation = None
        self.start_time = 0
        
    def start_animation(self, animation_type, **kwargs):
        """开始播放动画"""
        config = BATTLE_CONFIG['animations'][animation_type]
        self.current_animation = {
            'type': animation_type,
            'duration': config['duration'],
            'start_time': pygame.time.get_ticks(),
            'frame_count': config['frames'],
            **kwargs
        }
    
    def update(self, screen):
        """更新并绘制当前动画"""
        if not self.current_animation:
            return False
            
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.current_animation['start_time']
        
        if elapsed >= self.current_animation['duration']:
            self.current_animation = None
            return False
            
        # 计算当前帧
        progress = elapsed / self.current_animation['duration']
        frame = int(progress * self.current_animation['frame_count'])
        
        # 根据动画类型绘制不同效果
        if self.current_animation['type'] == 'attack':
            self._draw_attack_animation(screen, progress)
        elif self.current_animation['type'] == 'catch':
            self._draw_catch_animation(screen, progress)
        elif self.current_animation['type'] == 'evolution':
            self._draw_evolution_animation(screen, progress)
            
        return True
    
    def _draw_attack_animation(self, screen, progress):
        """绘制攻击动画"""
        start_pos = self.current_animation.get('start_pos')
        end_pos = self.current_animation.get('end_pos')
        if not (start_pos and end_pos):
            return
            
        # 计算当前位置
        current_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        current_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress
        
        # 绘制攻击效果
        size = 30
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(surface, (255, 0, 0, 128), (size//2, size//2), size//2)
        rect = surface.get_rect(center=(current_x, current_y))
        screen.blit(surface, rect) 
    
    def _draw_catch_animation(self, screen, progress):
        """绘制捕捉动画"""
        target_pos = self.current_animation.get('target_pos')
        if not target_pos:
            return
        
        size = 64
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # 动画分为三个阶段：
        # 1. 精灵球出现并变大 (0-0.3)
        # 2. 精灵球旋转 (0.3-0.7)
        # 3. 精灵球缩小并消失 (0.7-1.0)
        
        if progress < 0.3:
            # 阶段1：精灵球出现并变大
            scale = progress / 0.3
            ball_size = int(size * scale)
        elif progress < 0.7:
            # 阶段2：精灵球旋转
            ball_size = size
            rotation = (progress - 0.3) * 720  # 旋转两圈
        else:
            # 阶段3：精灵球缩小并消失
            scale = 1 - ((progress - 0.7) / 0.3)
            ball_size = int(size * scale)
        
        # 绘制精灵球
        pygame.draw.circle(surface, (255, 0, 0), (size//2, size//2), ball_size//2)  # 上半部分
        pygame.draw.circle(surface, (255, 255, 255), (size//2, size//2), ball_size//2, 2)  # 边框
        pygame.draw.line(surface, (0, 0, 0), (0, size//2), (size, size//2), 2)  # 中间线
        pygame.draw.circle(surface, (255, 255, 255), (size//2, size//2), ball_size//6)  # 中心按钮
        
        # 如果在旋转阶段，旋转精灵球
        if 0.3 <= progress < 0.7:
            surface = pygame.transform.rotate(surface, rotation)
        
        # 绘制到屏幕上
        rect = surface.get_rect(center=target_pos)
        screen.blit(surface, rect)
    
    def _draw_evolution_animation(self, screen, progress):
        """绘制进化动画"""
        # 这里需要实现进化动画的绘制逻辑
        pass