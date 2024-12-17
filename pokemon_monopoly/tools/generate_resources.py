import os
import pygame
import wave
import struct
import math

def create_directory_structure():
    """创建资源目录结构"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 创建目录
    directories = [
        'assets/sounds',
        'assets/music',
        'assets/images/effects/attack',
        'assets/images/effects/heal',
        'assets/images/effects/evolution',
        'assets/images/effects/catch',
        'assets/images/effects/teleport'
    ]
    
    for directory in directories:
        os.makedirs(os.path.join(base_dir, directory), exist_ok=True)

def generate_sound_effects():
    """生成基本音效"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sound_dir = os.path.join(base_dir, 'assets', 'sounds')
    
    # 生成各种音效
    sounds = {
        'battle_start': (440, 0.3),  # A4音符
        'attack': (880, 0.1),        # A5音符
        'hit': (220, 0.1),           # A3音符
        'victory': (660, 0.5),       # E5音符
        'defeat': (110, 0.5),        # A2音符
        'heal': (554, 0.3),          # C#5音符
        'level_up': (880, 0.5),      # A5音符
        'evolution': (1760, 1.0),    # A6音符
        'catch': (440, 0.2),         # A4音符
        'dice': (330, 0.1),          # E4音符
        'teleport': (587, 0.3),      # D5音符
        'button': (262, 0.1)         # C4音符
    }
    
    for name, (freq, duration) in sounds.items():
        _generate_wave_file(
            os.path.join(sound_dir, f'{name}.wav'),
            frequency=freq,
            duration=duration
        )

def _generate_wave_file(filename, frequency=440, duration=1.0, amplitude=0.5):
    """生成WAV音效文件"""
    # 设置参数
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    # 生成正弦波
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        value = int(32767 * amplitude * math.sin(2 * math.pi * frequency * t))
        samples.append(struct.pack('h', value))
    
    # 写入WAV文件
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(samples))

def generate_effect_images():
    """生成特效图片"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    effects_dir = os.path.join(base_dir, 'assets', 'images', 'effects')
    
    effects = {
        'attack': (255, 0, 0),      # 红色
        'heal': (0, 255, 0),        # 绿色
        'evolution': (255, 255, 0),  # 黄色
        'catch': (0, 0, 255),       # 蓝色
        'teleport': (255, 165, 0)   # 橙色
    }
    
    for effect_name, color in effects.items():
        effect_dir = os.path.join(effects_dir, effect_name)
        
        # 为每个特效生成6帧动画
        for i in range(1, 7):
            size = 64
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # 创建渐变效果
            alpha = int(255 * (1 - (i-1)/6))  # 透明度渐变
            scale = 1 + (i-1)/3  # 大小渐变
            
            # 绘制特效
            pygame.draw.circle(
                surface,
                (*color, alpha),
                (size//2, size//2),
                int(size//2 * scale)
            )
            
            # 保存帧
            pygame.image.save(surface, os.path.join(effect_dir, f'frame_{i}.png'))

def main():
    """主函数"""
    print("开始生成资源文件...")
    
    # 初始化pygame（用于生成图片）
    pygame.init()
    pygame.display.set_mode((1, 1))
    
    try:
        # 创建目录结构
        create_directory_structure()
        print("✓ 目录结构创建完成")
        
        # 生成音效
        generate_sound_effects()
        print("✓ 音效文件生成完成")
        
        # 生成特效图片
        generate_effect_images()
        print("✓ 特效图片生成完成")
        
    except Exception as e:
        print(f"错误：资源生成失败 - {str(e)}")
    
    print("资源生成完成！")
    pygame.quit()

if __name__ == "__main__":
    main() 