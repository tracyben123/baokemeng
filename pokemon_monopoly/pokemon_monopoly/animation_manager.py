import pygame
import math
import os

class AnimationManager:
    def __init__(self):
        self.animations = []
        self.effects = {}
        
        # 加载特效图片
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            effects_dir = os.path.join(base_dir, 'assets', 'images', 'effects')
            
            self.effects.update({
                'attack': self._load_effect_frames(os.path.join(effects_dir, 'attack')),
                'heal': self._load_effect_frames(os.path.join(effects_dir, 'heal')),
                'evolution': self._load_effect_frames(os.path.join(effects_dir, 'evolution')),
                'catch': self._load_effect_frames(os.path.join(effects_dir, 'catch')),
                'teleport': self._load_effect_frames(os.path.join(effects_dir, 'teleport'))
            })
            
            print("✓ 特效图片加载成功")
        except Exception as e:
            print(f"警告：特效图片加载失败 - {str(e)}")
            # 创建默认特效
            self._create_default_effects()
    
    def _create_default_effects(self):
        """创建默认特效"""
        size = 64
        frame_count = 6
        
        effects_data = {
            'attack': (255, 0, 0),      # 红色
            'heal': (0, 255, 0),        # 绿色
            'evolution': (255, 255, 0),  # 黄色
            'catch': (0, 0, 255),       # 蓝色
            'teleport': (255, 165, 0)   # 橙色
        }
        
        for effect_name, color in effects_data.items():
            frames = []
            for i in range(frame_count):
                # 创建帧
                surface = pygame.Surface((size, size), pygame.SRCALPHA)
                
                # 创建渐变效果
                alpha = int(255 * (1 - i/frame_count))  # 透明度渐变
                scale = 1 + i/3  # 大小渐变
                
                # 绘制特效
                pygame.draw.circle(
                    surface,
                    (*color, alpha),
                    (size//2, size//2),
                    int(size//2 * scale)
                )
                
                frames.append(surface)
            
            self.effects[effect_name] = frames
    
    def _load_effect_frames(self, directory):
        """加载特效帧动画"""
        frames = []
        i = 1
        while True:
            try:
                frame = pygame.image.load(os.path.join(directory, f'frame_{i}.png')).convert_alpha()
                frames.append(frame)
                i += 1
            except:
                break
        return frames
    
    def add_animation(self, animation_type, pos, duration=1000, **kwargs):
        """添加一个新动画"""
        # 检查特效是否存在且有效
        if animation_type not in self.effects or not self.effects[animation_type]:
            print(f"警告：特效 {animation_type} 不可用，创建默认特效")
            self._create_default_effect(animation_type)
        
        # 确保至少有一帧动画
        frame_count = len(self.effects[animation_type])
        if frame_count == 0:
            print(f"警告：特效 {animation_type} 没有帧，创建默认帧")
            self._create_default_effect(animation_type)
            frame_count = len(self.effects[animation_type])
        
        self.animations.append({
            'type': animation_type,
            'pos': pos,
            'start_time': pygame.time.get_ticks(),
            'duration': duration,
            'frame_index': 0,
            'frame_time': pygame.time.get_ticks(),
            'frame_duration': duration / frame_count,
            **kwargs
        })
    
    def _create_default_effect(self, effect_name):
        """创建默认特效"""
        size = 64
        frame_count = 6
        
        # 为不同特效类型选择不同颜色
        colors = {
            'attack': (255, 0, 0),      # 红色
            'heal': (0, 255, 0),        # 绿色
            'evolution': (255, 255, 0),  # 黄色
            'catch': (0, 0, 255),       # 蓝色
            'teleport': (255, 165, 0)   # 橙色
        }
        color = colors.get(effect_name, (200, 200, 200))  # 默认灰色
        
        frames = []
        for i in range(frame_count):
            # 创建帧
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # 创建渐变效果
            alpha = int(255 * (1 - i/frame_count))  # 透明度渐变
            scale = 1 + i/3  # 大小渐变
            
            # 绘制特效
            pygame.draw.circle(
                surface,
                (*color, alpha),
                (size//2, size//2),
                int(size//2 * scale)
            )
            
            frames.append(surface)
        
        self.effects[effect_name] = frames
    
    def update(self, screen):
        """更新并绘制所有动画"""
        current_time = pygame.time.get_ticks()
        completed = []
        
        for i, anim in enumerate(self.animations):
            # 检查动画是否完成
            if current_time - anim['start_time'] >= anim['duration']:
                completed.append(i)
                continue
            
            # 更新帧
            if current_time - anim['frame_time'] >= anim['frame_duration']:
                anim['frame_index'] = (anim['frame_index'] + 1) % len(self.effects[anim['type']])
                anim['frame_time'] = current_time
            
            # 绘制当前帧
            frame = self.effects[anim['type']][anim['frame_index']]
            
            # 特殊画效果
            if anim['type'] == 'attack':
                # 攻击动画：从起点移动到终点
                progress = (current_time - anim['start_time']) / anim['duration']
                start_pos = anim['start_pos']
                end_pos = anim['end_pos']
                current_pos = (
                    start_pos[0] + (end_pos[0] - start_pos[0]) * progress,
                    start_pos[1] + (end_pos[1] - start_pos[1]) * progress
                )
                pos = current_pos
            else:
                pos = anim['pos']
            
            # 绘制帧
            frame_rect = frame.get_rect(center=pos)
            screen.blit(frame, frame_rect)
        
        # 移除完成的动画
        for i in reversed(completed):
            self.animations.pop(i)
    
    def is_playing(self, animation_type=None):
        """检查是否有动画正在播放"""
        if animation_type:
            return any(a['type'] == animation_type for a in self.animations)
        return bool(self.animations) 