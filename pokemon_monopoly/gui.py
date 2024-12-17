import pygame
import os
import math
import random
import json
from datetime import datetime

class MinimalGUI:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        
        # 使用颜色常量替代图片
        self.colors = {
            'background': (240, 240, 240),  # 浅灰色背景
            'board': (255, 255, 255),       # 白色棋盘
            'pokemon_center': (255, 182, 193),  # 粉色表示宝可梦中心
            'gym': (152, 251, 152),         # 浅绿色表示道馆
            'shop': (135, 206, 235),        # 浅蓝色表示商店
            'wild_area': (189, 183, 107),   # 褐色表示野外区域
            'player1': (255, 0, 0),         # 红色表示玩家1
            'player2': (0, 0, 255),         # 蓝色表示玩家2
            'text': (0, 0, 0),               # 黑色文字
            'button': (200, 200, 200),
            'button_hover': (180, 180, 180),
            'hp_bar': (50, 205, 50),
            'money': (255, 215, 0)
        }
        
        # 使用系统默认字体
        self.font = pygame.font.SysFont(None, 32)
        
        # 添加UI状态
        self.ui_state = {
            'current_screen': 'main',  # main, battle, shop
            'selected_button': None,
            'hover_button': None
        }
        
        # 游戏状态
        self.game_states = {
            'main_menu': self.draw_main_menu,
            'game_board': self.draw_game_state,
            'battle': self.draw_battle,
            'shop': self.draw_shop,
            'pokemon_center': self.draw_pokemon_center
        }
        self.current_state = 'main_menu'
        
        # 按钮区域
        self.buttons = {}
    
    def draw(self):
        """根据当前状态绘制界面"""
        self.game_states[self.current_state]()
        pygame.display.flip()
        
    def draw_main_menu(self):
        """绘制主菜单"""
        self.screen.fill(self.colors['background'])
        
        # 绘制标题
        title = self.font.render('宝可梦大富翁', True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen_width//2, 200))
        self.screen.blit(title, title_rect)
        
        # 绘制菜单按钮
        menu_items = [
            ('开始游戏', 'start_game'),
            ('读取存档', 'load_game'),
            ('设置', 'settings'),
            ('退出', 'quit')
        ]
        
        self.buttons.clear()
        for i, (text, action) in enumerate(menu_items):
            button_rect = pygame.Rect(
                self.screen_width//2 - 100,
                300 + i * 60,
                200, 50
            )
            self.buttons[action] = button_rect
            
            # 绘制按钮
            pygame.draw.rect(self.screen, self.colors['button'], button_rect)
            pygame.draw.rect(self.screen, self.colors['text'], button_rect, 2)
            
            # 绘制文字
            text_surface = self.font.render(text, True, self.colors['text'])
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
            
    def draw_pokemon_center(self):
        """绘制宝可梦中心界面"""
        self.screen.fill(self.colors['background'])
        
        # 绘制标题
        title = self.font.render('宝可梦中心', True, self.colors['text'])
        self.screen.blit(title, (self.screen_width//2 - 100, 50))
        
        # 绘制玩家的宝可梦列表
        current_player = self.game.players[self.game.current_player]
        for i, pokemon in enumerate(current_player.pokemon_list):
            y = 150 + i * 80
            # 绘制宝可梦信息
            self._draw_pokemon_info(pokemon, (50, y))
            
        # 绘制返回按钮
        back_rect = pygame.Rect(50, self.screen_height - 70, 100, 40)
        self.buttons['back'] = back_rect
        pygame.draw.rect(self.screen, self.colors['button'], back_rect)
        back_text = self.font.render('返回', True, self.colors['text'])
        self.screen.blit(back_text, (70, self.screen_height - 60))
        
    def _draw_pokemon_info(self, pokemon, pos):
        """绘制宝可梦信息"""
        x, y = pos
        
        # 绘制名称和等级
        info_text = f"{pokemon.name} Lv.{pokemon.level}"
        text = self.font.render(info_text, True, self.colors['text'])
        self.screen.blit(text, (x, y))
        
        # 绘制HP条
        hp_ratio = pokemon.hp / pokemon.max_hp
        hp_width = 200
        pygame.draw.rect(self.screen, self.colors['hp_bar'],
                        (x, y + 30, hp_width * hp_ratio, 10))
        pygame.draw.rect(self.screen, self.colors['text'],
                        (x, y + 30, hp_width, 10), 1)
        
        # 绘制HP数值
        hp_text = f"{pokemon.hp}/{pokemon.max_hp}"
        hp_surface = self.font.render(hp_text, True, self.colors['text'])
        self.screen.blit(hp_surface, (x + hp_width + 10, y + 25))
        
    def draw_board(self):
        # 绘制背景
        self.screen.fill(self.colors['background'])
        
        # 绘制棋盘格子
        cell_size = 60
        for i in range(20):  # 假设20个格子
            x = 100 + (i * cell_size)
            y = 100
            pygame.draw.rect(self.screen, self.colors['board'], 
                           (x, y, cell_size, cell_size), 2)
            
            # 根据格子类型填充不同颜色
            cell_type = self.game.board[i].type
            if cell_type in self.colors:
                pygame.draw.rect(self.screen, self.colors[cell_type],
                               (x+2, y+2, cell_size-4, cell_size-4))
                               
    def draw_dice(self, number):
        # 使用文字显示骰子点数
        dice_text = self.font.render(str(number), True, self.colors['text'])
        self.screen.blit(dice_text, (self.screen_width//2, self.screen_height//2))
        
    def draw_pokemon(self, pokemon, pos):
        # 使用圆形和文字表示宝可梦
        pygame.draw.circle(self.screen, self.colors['player1'], pos, 20)
        name_text = self.font.render(pokemon.name, True, self.colors['text'])
        self.screen.blit(name_text, (pos[0]-30, pos[1]+25))
    
    def draw_player_info(self, player):
        # 绘制玩家信息（金钱、宝可梦等）
        info_text = f"金钱: {player.money}"
        text_surface = self.font.render(info_text, True, self.colors['text'])
        self.screen.blit(text_surface, (10, 10))
    
    def draw_menu(self):
        # 绘制游戏菜单
        menu_items = ['开始游戏', '设置', '退出']
        for i, item in enumerate(menu_items):
            y = 300 + i * 50
            text = self.font.render(item, True, self.colors['text'])
            self.screen.blit(text, (self.screen_width//2 - 50, y))
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # 检查按钮点击
            for action, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    self._handle_button_click(action)
                    
    def _handle_button_click(self, action):
        """处理按钮点击"""
        if action == 'start_game':
            self.current_state = 'game_board'
        elif action == 'load_game':
            # TODO: 实现读取存档
            pass
        elif action == 'settings':
            # TODO: 实现设置界面
            pass
        elif action == 'quit':
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif action == 'back':
            if self.current_state in ['pokemon_center', 'shop', 'battle']:
                self.current_state = 'game_board'
    
    def draw_game_state(self):
        """绘制完整游戏状态"""
        self.draw_board()
        self.draw_players()
        self.draw_current_player_info()
        self.draw_cell_info()
        
    def draw_players(self):
        """绘制所有玩家"""
        for i, player in enumerate(self.game.players):
            color = self.colors[f'player{i+1}']
            pos = self._get_player_position(player)
            pygame.draw.circle(self.screen, color, pos, 10)
            
    def draw_current_player_info(self):
        """绘制当前玩家信息"""
        player = self.game.players[self.game.current_player]
        info_text = [
            f"玩家: {player.name}",
            f"金钱: {player.money}",
            f"宝可梦: {len(player.pokemon_list)}/6",
            f"道具: {sum(player.items.values())}"
        ]
        
        for i, text in enumerate(info_text):
            surface = self.font.render(text, True, self.colors['text'])
            self.screen.blit(surface, (10, 10 + i * 30))
            
    def draw_cell_info(self):
        """绘制当前格子信息"""
        current_player = self.game.players[self.game.current_player]
        current_cell = self.game.board[current_player.position]
        
        info_text = [
            f"当前位置: {current_cell.name}",
            f"类型: {current_cell.type}"
        ]
        
        for i, text in enumerate(info_text):
            surface = self.font.render(text, True, self.colors['text'])
            self.screen.blit(surface, (self.screen_width - 200, 10 + i * 30))
    
    def draw_battle(self, battle):
        """绘制战斗界面"""
        # 清空屏幕
        self.screen.fill(self.colors['background'])
        
        # 绘制对战双方的宝可梦
        if battle.active_pokemon1:
            self._draw_battle_pokemon(battle.active_pokemon1, (200, 400), True)
        if battle.active_pokemon2:
            self._draw_battle_pokemon(battle.active_pokemon2, (600, 200), False)
            
        # 绘制技能按钮
        if battle.active_pokemon1 and battle.active_pokemon1.moves:
            self._draw_move_buttons(battle.active_pokemon1.moves)
            
    def _draw_battle_pokemon(self, pokemon, pos, is_player):
        """绘制战斗中的宝可梦"""
        # 绘制宝可梦
        pygame.draw.circle(self.screen, 
                         self.colors['player1' if is_player else 'player2'],
                         pos, 40)
                         
        # 绘制名称
        name_text = self.font.render(pokemon.name, True, self.colors['text'])
        self.screen.blit(name_text, (pos[0]-30, pos[1]-60))
        
        # 绘制HP条
        hp_ratio = pokemon.hp / pokemon.max_hp
        hp_width = 100
        pygame.draw.rect(self.screen, self.colors['hp_bar'],
                        (pos[0]-50, pos[1]-40, hp_width*hp_ratio, 10))
        pygame.draw.rect(self.screen, self.colors['text'],
                        (pos[0]-50, pos[1]-40, hp_width, 10), 1)
                        
    def _draw_move_buttons(self, moves):
        """绘制技能按钮"""
        for i, move in enumerate(moves):
            x = 50 + (i % 2) * 150
            y = 500 + (i // 2) * 50
            
            # 绘制按钮背景
            pygame.draw.rect(self.screen, self.colors['button'],
                           (x, y, 140, 40))
            
            # 绘制技能名称
            text = self.font.render(move.name, True, self.colors['text'])
            self.screen.blit(text, (x+10, y+10))