import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music = None
        self.enabled = True
        self.volume = 0.7
        
        # 加载音效
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sound_dir = os.path.join(base_dir, 'assets', 'sounds')
            
            # 加载战斗音效
            self.sounds.update({
                'battle_start': pygame.mixer.Sound(os.path.join(sound_dir, 'battle_start.wav')),
                'attack': pygame.mixer.Sound(os.path.join(sound_dir, 'attack.wav')),
                'hit': pygame.mixer.Sound(os.path.join(sound_dir, 'hit.wav')),
                'victory': pygame.mixer.Sound(os.path.join(sound_dir, 'victory.wav')),
                'defeat': pygame.mixer.Sound(os.path.join(sound_dir, 'defeat.wav')),
                'heal': pygame.mixer.Sound(os.path.join(sound_dir, 'heal.wav')),
                'level_up': pygame.mixer.Sound(os.path.join(sound_dir, 'level_up.wav')),
                'evolution': pygame.mixer.Sound(os.path.join(sound_dir, 'evolution.wav')),
                'catch': pygame.mixer.Sound(os.path.join(sound_dir, 'catch.wav')),
                'dice': pygame.mixer.Sound(os.path.join(sound_dir, 'dice.wav')),
                'teleport': pygame.mixer.Sound(os.path.join(sound_dir, 'teleport.wav')),
                'button': pygame.mixer.Sound(os.path.join(sound_dir, 'button.wav'))
            })
            
            # 设置音量
            for sound in self.sounds.values():
                sound.set_volume(self.volume)
            
            print("✓ 音效加载成功")
        except Exception as e:
            print(f"警告：音效加载失败 - {str(e)}")
            self.enabled = False
    
    def play_sound(self, sound_name):
        """播放音效"""
        if self.enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def play_music(self, music_name):
        """播放背景音乐"""
        if not self.enabled:
            return
        
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            music_path = os.path.join(base_dir, 'assets', 'music', f'{music_name}.mp3')
            
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self.volume * 0.5)  # 背景音乐音量稍低
            pygame.mixer.music.play(-1)  # -1表示循环播放
        except Exception as e:
            print(f"警告：背景音乐加载失败 - {str(e)}")
    
    def stop_music(self):
        """停止背景音乐"""
        if self.enabled:
            pygame.mixer.music.stop()
    
    def set_volume(self, volume):
        """设置音量"""
        self.volume = max(0.0, min(1.0, volume))
        if self.enabled:
            for sound in self.sounds.values():
                sound.set_volume(self.volume)
            pygame.mixer.music.set_volume(self.volume * 0.5) 