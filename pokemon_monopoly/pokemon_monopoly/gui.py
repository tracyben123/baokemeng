import pygame
import os
import math
from .sound_manager import SoundManager
from .animation_manager import AnimationManager
from .battle_animation_manager import BattleAnimationManager
from .player import Player
from .game_enums import TurnState, EventType
from .battle import Battle  # 添加这行导入

class MinimalGUI:
    def __init__(self, game):
        pygame.init()
        self.game = game
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('宝可梦大富翁')
        
        # 加载字体
        try:
            # 使用绝对路径加载字体
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            font_dir = os.path.join(base_dir, 'assets', 'fonts')
            
            self.title_font = pygame.font.Font(
                os.path.join(font_dir, 'SourceHanSansSC-Bold.otf'), 32
            )
            self.button_font = pygame.font.Font(
                os.path.join(font_dir, 'SourceHanSansSC-Regular.otf'), 24
            )
            self.text_font = pygame.font.Font(
                os.path.join(font_dir, 'SourceHanSansSC-Regular.otf'), 16
            )
            print("✓ 字体加载成功")
        except Exception as e:
            print(f"警告：字体加载失败 - {str(e)}")
            print("使用系统默认字体")
            self.title_font = pygame.font.SysFont(None, 32)
            self.button_font = pygame.font.SysFont(None, 24)
            self.text_font = pygame.font.SysFont(None, 16)
        
        # 使用颜色常量替代图片
        self.colors = {
            'background': (240, 240, 240),  # 浅灰色背景
            'board': (255, 255, 255),       # 白色棋盘
            'pokemon_center': (255, 182, 193),  # 粉色表示宝可梦中心
            'gym': (152, 251, 152),         # 浅绿色表示道馆
            'shop': (135, 206, 235),        # 浅蓝色表示商店
            'wild_area': (189, 183, 107),   # 褐色表示野外区域
            'special': (147, 112, 219),     # 紫色表示特殊格子
            'teleport': (255, 165, 0),      # 橙色表示传送格子
            'player1': (255, 0, 0),         # 红色表示玩家1
            'player2': (0, 0, 255),         # 蓝色表示玩家2
            'text': (0, 0, 0),              # 黑色文字
            'button': (200, 200, 200),      # 按钮颜色
            'button_hover': (180, 180, 180),# 按钮悬停颜��
            'hp_bar': (50, 205, 50),        # 生命值颜色
            'money': (255, 215, 0)          # 金钱颜色
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
        
        # 操作提示
        self.tips = {
            'main_menu': '点击按钮选择操作',
            'game_board': '按空格键投骰子，移动角色',
            'battle': '点击技能按钮进行战斗',
            'shop': '点击物品进行购买',
            'pokemon_center': '点击宝可梦进行恢复'
        }
        
        # 加载宝可梦图片
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            pokemon_dir = os.path.join(base_dir, 'assets', 'images', 'pokemon')
            
            # 加载所有宝可梦图片
            self.pokemon_images = {}
            pokemon_list = [
                'pikachu',      # 皮卡丘
                'charmander',   # 小火龙
                'squirtle',     # 杰尼龟
                'bulbasaur',    # 妙蛙种子
                'eevee',        # 伊布
                'meowth',       # 喵喵
                'psyduck',      # 可达鸭
                'growlithe'     # 卡蒂狗
            ]
            
            for pokemon_id in pokemon_list:
                try:
                    self.pokemon_images[pokemon_id] = {
                        'battle': pygame.image.load(os.path.join(pokemon_dir, f'{pokemon_id}_battle.png')).convert_alpha(),
                        'board': pygame.image.load(os.path.join(pokemon_dir, f'{pokemon_id}_board.png')).convert_alpha(),
                        'avatar': pygame.image.load(os.path.join(pokemon_dir, f'{pokemon_id}_avatar.png')).convert_alpha()
                    }
                    print(f"✓ 加载宝可梦图片: {pokemon_id}")
                except Exception as e:
                    print(f"警告：{pokemon_id}图片加载失败 - {str(e)}")
                    # 为加载失败的宝可梦创建默认图片
                    self.pokemon_images[pokemon_id] = {
                        'battle': self._create_default_pokemon_image((128, 128), pokemon_id),
                        'board': self._create_default_pokemon_image((64, 64), pokemon_id),
                        'avatar': self._create_default_pokemon_image((32, 32), pokemon_id)
                    }  # 添加缺失的右花括号
            
            print("✓ 宝可梦图片加载完成")
        except Exception as e:
            print(f"警告：宝可梦图片加载失败 - {str(e)}")
            self.pokemon_images = {}
        
        # 设置默认UI属性
        self.use_default_ui = False
        self.frames = {}
        self.button_images = {}
        self.icons = {}
        
        # 加载UI资源
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ui_dir = os.path.join(base_dir, 'assets', 'images', 'ui')
            
            # 加载按钮
            self.button_images = {
                'normal': pygame.image.load(os.path.join(ui_dir, 'buttons', 'button_normal.png')).convert_alpha(),
                'hover': pygame.image.load(os.path.join(ui_dir, 'buttons', 'button_hover.png')).convert_alpha(),
                'pressed': pygame.image.load(os.path.join(ui_dir, 'buttons', 'button_pressed.png')).convert_alpha()
            }
            
            # 加载框
            self.frames = {
                'dialog': pygame.image.load(os.path.join(ui_dir, 'frames', 'frame_dialog.png')).convert_alpha(),
                'menu': pygame.image.load(os.path.join(ui_dir, 'frames', 'frame_menu.png')).convert_alpha(),
                'status': pygame.image.load(os.path.join(ui_dir, 'frames', 'frame_status.png')).convert_alpha()
            }
            
            # 加载图标
            self.icons = {
                'money': pygame.image.load(os.path.join(ui_dir, 'icons', 'icon_money.png')).convert_alpha(),
                'hp': pygame.image.load(os.path.join(ui_dir, 'icons', 'icon_hp.png')).convert_alpha()
            }
            
            print("✓ UI资源加载成功")
        except Exception as e:
            print(f"警告：UI资源加载失败 - {str(e)}")
            self.use_default_ui = True
        
        # 加载游戏板资源
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            board_dir = os.path.join(base_dir, 'assets', 'images', 'board')
            
            # 加载背景地图
            self.board_background = pygame.image.load(
                os.path.join(board_dir, 'board_background.png')
            ).convert_alpha()
            print("✓ 游戏板背景加载成功")
        except Exception as e:
            print(f"警告：游戏板背景加载失败 - {str(e)}")
            # 创建默认背景
            self.board_background = self._create_default_image(
                (self.screen_width, self.screen_height),
                (220, 255, 220)  # 添加右括号
            )
        
        # 添加移动动画相关属性
        self.moving_player = False
        self.move_start_time = 0
        self.move_duration = 1000  # 移动动画持续时间（毫秒）
        self.move_start_pos = None
        self.move_target_pos = None
        self.move_progress = 0
        self.steps_left = 0
        self.step_duration = 300  # 每步移动时间（毫秒）
        
        # 添加传送动画相关属性
        self.teleporting = False
        self.teleport_start_time = 0
        self.teleport_duration = 1000  # 传送动画持续时间（毫秒）
        self.teleport_flash_count = 5  # 闪烁次数
        
        # 添加骰子相关属性
        self.rolling_dice = False
        self.dice_roll_start_time = 0
        self.dice_result = None
        self.last_dice_result = None
        self.dice_frame_index = 0
        self.roll_duration = 1000  # 骰子动画持续时间（毫秒）
        self.dice_frames = []  # 骰子动画帧列表
        
        # 创建默认骰子图片
        for i in range(1, 7):
            dice_surface = self._create_default_dice(i)
            self.dice_frames.append(dice_surface)
        
        # 加载骰子图片
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            dice_dir = os.path.join(base_dir, 'assets', 'images', 'dice')
            for i in range(1, 7):
                img = pygame.image.load(os.path.join(dice_dir, f'dice_{i}.png')).convert_alpha()
                self.dice_frames[i-1] = img  # 替换默认图片
            print("✓ 骰子图片加载成功")
        except Exception as e:
            print(f"警告：骰子图片加载失败 - {str(e)}")
            # 已经创建了默认骰子图片，不需要额外处理
        
        # 添加音效和动画管理器
        self.sound_manager = SoundManager()
        self.animation_manager = AnimationManager()
        self.battle_animation_manager = BattleAnimationManager()  # 添加战斗动画管理器
        
        # 播放主菜单音乐
        self.sound_manager.play_music('title')
        
        # 添加警告缓存
        self.warned_pokemon = set()  # 用于记录已经警告过的宝可梦
        
        # 添加回合控制
        self.turn_ended = False  # 标记当前回合是否结束
        
        # 修改回合控制
        self.can_roll_dice = True  # 标记当前玩家是否可以投骰子
        
        # 回合控制
        self.turn_state = TurnState.READY
        self.current_event = None
        self.steps_left = 0
        
        # 动画控制
        self.animation_timer = 0
        self.animation_duration = {
            'roll': 1000,    # 骰子动画持续时间
            'move': 300,     # 每步移动时间
            'teleport': 1000 # 传送动画时间
        }
    
    def _create_default_image(self, size, color):
        """创建默认图片（用于图片加载失败时）"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect())
        return surface
    
    def draw(self):
        """根据当前状态绘制界面"""
        self.game_states[self.current_state]()
        pygame.display.flip()
    
    def draw_board(self):
        """绘制游戏棋盘"""
        # 清空背景
        self.screen.fill(self.colors['background'])
        
        # 计算游戏板大小（留出边距）
        margin = 60  # 减小边距以便增大可用空间
        board_width = self.screen_width - (margin * 2)
        board_height = self.screen_height - (margin * 2)
        
        # 等比例缩放背景图片
        original_ratio = self.board_background.get_width() / self.board_background.get_height()
        if board_width / board_height > original_ratio:
            scaled_height = board_height
            scaled_width = board_height * original_ratio
        else:
            scaled_width = board_width
            scaled_height = board_width / original_ratio
        
        # 缩放背景图片
        scaled_background = pygame.transform.scale(self.board_background, (int(scaled_width), int(scaled_height)))
        
        background_rect = scaled_background.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(scaled_background, background_rect)
        
        # 添加半透明云雾图层
        fog_surface = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        fog_surface.fill((255, 255, 255, 180))  # 白色半透明
        self.screen.blit(fog_surface, background_rect)
        
        # 调整边和可用空
        margin_x = scaled_width * 0.1
        margin_y = scaled_height * 0.1
        
        # 计算实际用区域
        usable_width = scaled_width - (margin_x * 2)
        usable_height = scaled_height - (margin_y * 2)
        
        # 调整格子大小和距
        cell_size = min(usable_width / 14, usable_height / 14)  # 增大格子尺寸
        gap = cell_size * 0.3  # 格子间隙
        
        # 计算中心点
        center_x = background_rect.centerx
        center_y = background_rect.centery
        
        # 计算个圈的半径
        outer_radius_x = usable_width * 0.42  # 外圈稍微扩大
        outer_radius_y = usable_height * 0.42
        inner_radius_x = usable_width * 0.22  # 内圈稍微缩小
        inner_radius_y = usable_height * 0.22
        
        # 清空位置列表
        self.cell_positions = {'outer': [], 'inner': []}
        
        # 绘制外圈格子（24个格子）
        for i in range(24):
            angle = 2 * math.pi * i / 24
            x = center_x + math.cos(angle) * outer_radius_x
            y = center_y + math.sin(angle) * outer_radius_y
            
            # 存储格子位置
            self.cell_positions['outer'].append((x, y))
            
            # 绘制格子
            cell_rect = pygame.Rect(x - cell_size/2, y - cell_size/2, cell_size, cell_size)
            cell_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            
            # 如果是传送格子，使用特殊效果
            if i == self.game.outer_teleport_pos:
                color = (*self.colors['teleport'], 230)
                pygame.draw.rect(cell_surface, color, cell_surface.get_rect(), border_radius=5)
                # 添加传送效果
                pygame.draw.polygon(cell_surface, (255, 215, 0), [
                    (cell_size/2, 0), 
                    (cell_size, cell_size/2),
                    (cell_size/2, cell_size),
                    (0, cell_size/2)
                ])
            else:
                cell_type = self.game.outer_circle[i].type
                color = self.colors[cell_type]
                pygame.draw.rect(cell_surface, (*color, 230), cell_surface.get_rect(), border_radius=5)
            
            self.screen.blit(cell_surface, cell_rect)
            
            # 绘制格子名称
            text = self.text_font.render(self.game.outer_circle[i].name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # 绘制内圈格子（16个格）
        for i in range(16):
            angle = 2 * math.pi * i / 16
            x = center_x + math.cos(angle) * inner_radius_x
            y = center_y + math.sin(angle) * inner_radius_y
            
            # 存储格子位置
            self.cell_positions['inner'].append((x, y))
            
            # 绘制格子
            cell_rect = pygame.Rect(x - cell_size/2, y - cell_size/2, cell_size, cell_size)
            cell_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            
            # 如果是传送格子，使用���殊效果
            if i == self.game.inner_teleport_pos:
                color = (*self.colors['teleport'], 230)
                pygame.draw.rect(cell_surface, color, cell_surface.get_rect(), border_radius=5)
                # 添加传送效果
                pygame.draw.polygon(cell_surface, (255, 215, 0), [
                    (cell_size/2, 0), 
                    (cell_size, cell_size/2),
                    (cell_size/2, cell_size),
                    (0, cell_size/2)
                ])
            else:
                cell_type = self.game.inner_circle[i].type
                color = self.colors[cell_type]
                pygame.draw.rect(cell_surface, (*color, 230), cell_surface.get_rect(), border_radius=5)
            
            self.screen.blit(cell_surface, cell_rect)
            
            # 绘制格子名称
            text = self.text_font.render(self.game.inner_circle[i].name, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, text_rect)
        
        # 绘制玩家
        self.draw_players()
    
    def draw_main_menu(self):
        """使用新UI元素绘制主菜单"""
        self.screen.fill(self.colors['background'])
        
        # 绘制菜单框架
        menu_rect = pygame.Rect(
            self.screen_width//2 - 150,
            100,
            300,
            500
        )
        self.draw_frame('menu', menu_rect)
        
        # 绘制题
        title = self.title_font.render('宝可梦大富翁', True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen_width//2, 150))
        self.screen.blit(title, title_rect)
        
        # 绘制按钮
        menu_items = [
            ('开始游戏', 'start_game'),
            ('读取存档', 'load_game'),
            ('游戏设置', 'settings'),
            ('退出游戏', 'quit')
        ]
        
        self.buttons.clear()
        for i, (text, action) in enumerate(menu_items):
            button_rect = pygame.Rect(
                self.screen_width//2 - 100,
                300 + i * 60,
                200, 50
            )
            self.buttons[action] = button_rect
            
            # 检查鼠标停状态
            mouse_pos = pygame.mouse.get_pos()
            state = 'hover' if button_rect.collidepoint(mouse_pos) else 'normal'
            
            # 使用新的按钮绘制方法
            self.draw_button(text, button_rect, state)
    
    def draw_game_state(self):
        """绘制游戏主界面"""
        # 绘制棋盘
        self.draw_board()
        
        # 绘制玩家
        self.draw_players()
        
        # 更新玩家移动
        self.update_player_movement()
        
        # 更新传送动画
        self.update_teleport_animation()
        
        # 绘制骰子（确保在其他元素之上）
        if self.rolling_dice or self.last_dice_result is not None:
            self.draw_dice()
        
        # 绘制格子信息
        self.draw_cell_info()
        
        # 绘制当前玩家信息
        self.draw_current_player_info()
        
        # 绘制操作提示
        tip = self.text_font.render(self.tips['game_board'], True, self.colors['text'])
        tip_rect = tip.get_rect(center=(self.screen_width//2, 30))
        self.screen.blit(tip, tip_rect)
    
    def draw_players(self):
        """绘制所有玩家"""
        current_time = pygame.time.get_ticks()
        
        for i, player in enumerate(self.game.players):
            # 根据玩家所在的圈获取正确的位置
            if player.circle == 'outer':
                if player.position < len(self.cell_positions['outer']):
                    x, y = self.cell_positions['outer'][player.position]
            else:
                if player.position < len(self.cell_positions['inner']):
                    x, y = self.cell_positions['inner'][player.position]
            
            # 绘制玩家
            player_color = self.colors[f'player{i+1}']
            player_size = min(self.screen_width, self.screen_height) // 25
            
            # 创建玩家标记
            player_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
            
            # 如果是当前玩家，添加动态效果
            if i == self.game.current_player:
                # 呼吸效果
                pulse = math.sin(current_time * 0.005) * 0.2 + 1.0  # 产生0.8到1.2的缩放
                glow_size = int(player_size * pulse)
                
                # 绘制光环
                glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (*player_color, 100),  # 半透明光环
                                 (glow_size//2, glow_size//2), 
                                 glow_size//2)
                glow_rect = glow_surface.get_rect(center=(x, y))
                self.screen.blit(glow_surface, glow_rect)
                
                # 当前玩家的标稍大一些
                actual_size = int(player_size * 1.2)
            else:
                actual_size = player_size
            
            # 绘制玩家标记
            pygame.draw.circle(player_surface, (*player_color, 230), 
                             (player_size//2, player_size//2), 
                             actual_size//2)
            
            # 添加边框
            pygame.draw.circle(player_surface, (255, 255, 255, 200), 
                             (player_size//2, player_size//2), 
                             actual_size//2, 2)
            
            # 在玩家标记中添加编号
            player_num = self.text_font.render(str(i+1), True, (255, 255, 255))
            num_rect = player_num.get_rect(center=(player_size//2, player_size//2))
            player_surface.blit(player_num, num_rect)
            
            # 绘制玩家标记
            player_rect = player_surface.get_rect(center=(x, y))
            self.screen.blit(player_surface, player_rect)
    
    def _get_player_position(self, player):
        """获取玩家棋盘上的像素位置"""
        cell_size = min(self.screen_width, self.screen_height) // 8
        start_x = (self.screen_width - cell_size * 6) // 2
        start_y = (self.screen_height - cell_size * 6) // 2
        
        pos = player.position
        if pos < 5:  # 上边
            x = start_x + pos * cell_size + cell_size//2
            y = start_y + cell_size//2
        elif pos < 10:  # 右边
            x = start_x + 4 * cell_size + cell_size//2
            y = start_y + (pos - 5) * cell_size + cell_size//2
        elif pos < 15:  # 下边
            x = start_x + (14 - pos) * cell_size + cell_size//2
            y = start_y + 4 * cell_size + cell_size//2
        else:  # 左边
            x = start_x + cell_size//2
            y = start_y + (19 - pos) * cell_size + cell_size//2
            
        return (x, y)
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            print(f"\n[点击事件] 当前状态: {self.current_state}, 当前玩家: {self.game.current_player + 1}")
            print(f"[点击事件] 位置: {mouse_pos}")
            
            # 根据当前状态处理点击事件
            if self.current_state == 'main_menu':
                print("[点击事件] 处理主菜单点击")
                self._handle_menu_click(mouse_pos)
            elif self.current_state == 'game_board':
                print(f"[点击事件] 处理游戏板点击")
                print(f"[状态] 移动中: {self.moving_player}, 投骰中: {self.rolling_dice}, 可投骰: {self.can_roll_dice}")
                self._handle_board_click(mouse_pos)
            elif self.current_state == 'battle':
                print("[点击事件] 处理战斗点击")
                self._handle_battle_click(mouse_pos)
            elif self.current_state == 'shop':
                print("[点击事件] 处理商店点击")
                self._handle_shop_click(mouse_pos)
            elif self.current_state == 'pokemon_center':
                print("[点击事件] 处理宝可梦中心点击")
                self._handle_pokemon_center_click(mouse_pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.current_state == 'game_board':
                self._handle_dice_roll()
    
    def _handle_button_click(self, action):
        """处理按钮点击"""
        if action == 'start_game':
            self.current_state = 'game_board'
            # 播放游戏开始音乐
            self.sound_manager.play_music('game_background')
        elif action == 'load_game':
            # TODO: 实现取存档
            pass
        elif action == 'settings':
            # TODO: 实现设置界面
            pass
        elif action == 'quit':
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        elif action == 'back':
            if self.current_state in ['pokemon_center', 'shop', 'battle']:
                self.current_state = 'game_board'
        elif action == 'back_to_menu':
            self.current_state = 'main_menu'
            self.sound_manager.play_music('title')
    
    def draw_current_player_info(self):
        """绘制当前玩家信息"""
        player = self.game.players[self.game.current_player]
        
        # 左上角显示玩家基本信息
        info_rect = pygame.Rect(10, 10, 200, 120)
        if not self.use_default_ui:
            self.draw_frame('status', info_rect)
        else:
            pygame.draw.rect(self.screen, self.colors['background'], info_rect)
            pygame.draw.rect(self.screen, self.colors['text'], info_rect, 2)
        
        # 绘制玩家标记
        color = self.colors[f'player{self.game.current_player+1}']
        pygame.draw.circle(self.screen, color, (30, 30), 10)
        
        # 绘制玩家基本信息
        info_text = [
            f"玩家 {self.game.current_player+1}",
            f"金钱: {player.money}",
            f"道具: {sum(player.items.values())}"
        ]
        
        for i, text in enumerate(info_text):
            surface = self.text_font.render(text, True, self.colors['text'])
            self.screen.blit(surface, (50, 20 + i * 25))
        
        # 右侧显示宝可梦列表
        pokemon_list_rect = pygame.Rect(self.screen_width - 220, 10, 200, 300)
        if not self.use_default_ui:
            self.draw_frame('status', pokemon_list_rect)
        else:
            pygame.draw.rect(self.screen, self.colors['background'], pokemon_list_rect)
            pygame.draw.rect(self.screen, self.colors['text'], pokemon_list_rect, 2)
        
        # 绘制宝可梦列表标题
        title = self.text_font.render("我的宝可梦", True, self.colors['text'])
        title_rect = title.get_rect(centerx=pokemon_list_rect.centerx, top=pokemon_list_rect.top + 10)
        self.screen.blit(title, title_rect)
        
        # 绘制宝可梦列表
        for i, pokemon in enumerate(player.pokemon_list):
            y = pokemon_list_rect.top + 40 + i * 50
            
            # 绘制宝可梦图标
            if pokemon.species in self.pokemon_images:
                image = self.pokemon_images[pokemon.species]['avatar']
            else:
                image = self._create_default_pokemon_image((32, 32), pokemon.species)
            image_rect = image.get_rect(left=pokemon_list_rect.left + 10, centery=y + 10)
            self.screen.blit(image, image_rect)
            
            # 绘制宝可梦信息
            info_text = f"{pokemon.name} Lv.{pokemon.level}"
            text = self.text_font.render(info_text, True, self.colors['text'])
            self.screen.blit(text, (image_rect.right + 10, y))
            
            # 绘制HP条
            hp_ratio = pokemon.current_hp / pokemon.stats['hp']
            hp_color = (50, 205, 50) if hp_ratio > 0.5 else (255, 140, 0) if hp_ratio > 0.2 else (220, 20, 60)
            hp_rect = pygame.Rect(image_rect.right + 10, y + 20, 100, 8)
            pygame.draw.rect(self.screen, (128, 128, 128), hp_rect, border_radius=4)
            if hp_ratio > 0:
                pygame.draw.rect(self.screen, hp_color,
                               (hp_rect.left, hp_rect.top, hp_rect.width * hp_ratio, hp_rect.height),
                               border_radius=4)
    
    def draw_cell_info(self):
        """绘制当前格子信息"""
        current_player = self.game.players[self.game.current_player]
        
        # 根据玩家在圈获取当前格子
        if current_player.circle == 'outer':
            current_cell = self.game.outer_circle[current_player.position]
        else:
            current_cell = self.game.inner_circle[current_player.position]
        
        # 制格子信息
        info_text = [
            f"当前位置：{current_cell.name}",
            f"类型：{current_cell.type}"
        ]
        
        for i, text in enumerate(info_text):
            surface = self.text_font.render(text, True, self.colors['text'])
            rect = surface.get_rect(topright=(self.screen_width - 20, 20 + i * 30))
            self.screen.blit(surface, rect)
    
    def draw_battle(self):
        """绘制战斗界面"""
        # 绘制背景
        self.screen.fill(self.colors['background'])
        
        # 获取战斗对象和当前玩家
        battle = self.game.current_battle
        current_player = self.game.get_current_player()
        
        # 显示当前玩家信息
        player_text = self.text_font.render(f"{current_player.name}的回合", True, (0, 0, 0))
        text_rect = player_text.get_rect(centerx=self.screen_width//2, top=10)
        self.screen.blit(player_text, text_rect)
        
        # 获取战斗对家
        player_pokemon = battle.player_pokemon
        enemy_pokemon = battle.enemy_pokemon
        
        # 布局参数
        player_area = {
            'x': self.screen_width * 0.25,  # 玩家宝可梦在左侧
            'y': self.screen_height * 0.6,  # 位置低
            'info_y': self.screen_height * 0.45  # 信息显示在宝可梦上方
        }
        
        enemy_area = {
            'x': self.screen_width * 0.75,  # 敌方宝可梦在右侧
            'y': self.screen_height * 0.3,  # 位置稍高
            'info_y': self.screen_height * 0.15  # 信息显示在宝可梦上方
        }
        
        # 绘制宝可梦和信息
        self._draw_pokemon_battle_info(player_pokemon, player_area, True)
        self._draw_pokemon_battle_info(enemy_pokemon, enemy_area, False)
        
        # 绘制操作区域（底部）
        button_area = pygame.Rect(0, self.screen_height * 0.75, 
                                self.screen_width, self.screen_height * 0.25)
        pygame.draw.rect(self.screen, (240, 240, 240), button_area)
        
        # 清空按钮字典
        self.buttons = {}
        
        # 绘制技能按钮（左侧）
        moves_area = pygame.Rect(20, button_area.top + 10, 
                               self.screen_width * 0.6 - 20, button_area.height - 20)
        self._draw_move_buttons(player_pokemon, moves_area)
        
        # 绘制功能按钮（右侧）
        action_area = pygame.Rect(self.screen_width * 0.6 + 20, button_area.top + 10,
                                self.screen_width * 0.4 - 40, button_area.height - 20)
        self._draw_battle_action_buttons(battle, action_area)
        
        # 绘制战斗消息（按钮����������������上方）
        message_area = pygame.Rect(20, button_area.top - 60, 
                                 self.screen_width - 40, 50)
        self._draw_battle_messages(battle.messages, message_area)
        
        # 更新显示
        pygame.display.flip()
    
    def _draw_pokemon_battle_info(self, pokemon, area, is_player):
        """绘制战��中的宝��梦信息"""
        # 绘制宝可���图片
        if pokemon.species in self.pokemon_images:
            image = self.pokemon_images[pokemon.species]['battle']
        else:
            image = self._create_default_pokemon_image((128, 128), pokemon.species)
        
        if not is_player:
            image = pygame.transform.flip(image, True, False)
        
        image_rect = image.get_rect(center=(area['x'], area['y']))
        self.screen.blit(image, image_rect)
        
        # 绘制信息面板
        info_panel = pygame.Surface((300, 100), pygame.SRCALPHA)
        pygame.draw.rect(info_panel, (255, 255, 255, 200), info_panel.get_rect(), border_radius=10)
        
        # ���制名称和等级
        name_text = self.text_font.render(f"{pokemon.name} Lv.{pokemon.level}", True, (0, 0, 0))
        info_panel.blit(name_text, (10, 10))
        
        # 绘制HP条
        hp_ratio = pokemon.current_hp / pokemon.stats['hp']
        hp_color = (50, 205, 50) if hp_ratio > 0.5 else (255, 140, 0) if hp_ratio > 0.2 else (220, 20, 60)
        
        pygame.draw.rect(info_panel, (128, 128, 128), (10, 40, 280, 15), border_radius=5)
        if hp_ratio > 0:
            pygame.draw.rect(info_panel, hp_color, (10, 40, 280 * hp_ratio, 15), border_radius=5)
        
        hp_text = self.text_font.render(f"{pokemon.current_hp}/{pokemon.stats['hp']}", True, (0, 0, 0))
        info_panel.blit(hp_text, (10, 60))
        
        # 如果是玩家的宝可梦，显示PP信息
        if is_player:
            pp_info = []
            for move in pokemon.moves:
                # 修复括号匹配问题
                current_pp = pokemon.current_pp[move['name']]
                max_pp = move['pp']
                pp_info.append(f"{move['name']}: {current_pp}/{max_pp} PP")
            
            pp_panel = pygame.Surface((200, len(pp_info) * 25 + 10), pygame.SRCALPHA)
            pygame.draw.rect(pp_panel, (255, 255, 255, 200), pp_panel.get_rect(), border_radius=5)
            
            for i, text in enumerate(pp_info):
                pp_text = self.text_font.render(text, True, (0, 0, 0))
                pp_panel.blit(pp_text, (10, 10 + i * 25))
            
            # 修复括号错误
            pp_rect = pp_panel.get_rect(left=image_rect.right + 20, centery=area['y'])
            self.screen.blit(pp_panel, pp_rect)
        
        # 绘制信息面板
        info_rect = info_panel.get_rect(centerx=area['x'], top=area['info_y'])
        self.screen.blit(info_panel, info_rect)
    
    def draw_shop(self):
        """绘制商店界面"""
        self.screen.fill(self.colors['background'])
        
        # 绘制标题
        title = self.title_font.render('商店', True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        self.screen.blit(title, title_rect)
        
        # 绘制操作提示
        tip = self.text_font.render(self.tips['shop'], True, self.colors['text'])
        tip_rect = tip.get_rect(center=(self.screen_width//2, 100))
        self.screen.blit(tip, tip_rect)
        
        # 清空按钮字典
        self.buttons = {}
        
        # 绘制商品列表
        items = [
            ('精灵球', 'pokeball', 100),
            ('药水', 'potion', 50),
            ('进化石', 'evolution_stone', 200)
        ]
        
        for i, (name, item_id, price) in enumerate(items):
            button_rect = pygame.Rect(
                self.screen_width//2 - 100,
                200 + i * 60,
                200, 50
            )
            self.buttons[f'buy_{item_id}'] = button_rect
            
            # 绘制商品按钮
            pygame.draw.rect(self.screen, self.colors['button'], button_rect, border_radius=5)
            text = self.text_font.render(f"{name} - {price}金币", True, (0, 0, 0))
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)
        
        # 添加返回按钮
        back_rect = pygame.Rect(10, self.screen_height - 60, 100, 40)
        self.buttons['back'] = back_rect
        pygame.draw.rect(self.screen, self.colors['button'], back_rect, border_radius=5)
        back_text = self.text_font.render("返回", True, (0, 0, 0))
        text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, text_rect)
    
    def draw_pokemon_center(self):
        """绘制宝可梦中心界面"""
        self.screen.fill(self.colors['background'])
        
        # 绘制标题
        title = self.title_font.render('宝可梦中心', True, self.colors['text'])
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        self.screen.blit(title, title_rect)
        
        # 获取进入宝可梦中心的玩家
        current_player = self.game.players[self.game.current_player]
        
        # 绘制该玩家的宝可梦列表
        pokemon_list = current_player.pokemon_list
        for i, pokemon in enumerate(pokemon_list):
            # 计算位置
            x = self.screen_width//4 + (i % 2) * (self.screen_width//2)
            y = 150 + (i // 2) * 120
            
            # 创建宝可梦卡片背景
            card_rect = pygame.Rect(x-80, y-30, 160, 100)
            pygame.draw.rect(self.screen, (255, 255, 255, 200), card_rect, border_radius=10)
            
            # 绘制宝可梦图片
            if pokemon.species in self.pokemon_images:
                image = self.pokemon_images[pokemon.species]['avatar']
            else:
                image = self._create_default_pokemon_image((32, 32), pokemon.species)
            
            image_rect = image.get_rect(center=(x-60, y))
            self.screen.blit(image, image_rect)
            
            # 绘制宝可梦信息
            info_text = [
                f"{pokemon.name} Lv.{pokemon.level}",
                f"HP: {pokemon.current_hp}/{pokemon.stats['hp']}"
            ]
            
            for j, text in enumerate(info_text):
                surface = self.text_font.render(text, True, self.colors['text'])
                self.screen.blit(surface, (x-30, y-10+j*20))
            
            # 绘制HP条
            hp_ratio = pokemon.current_hp / pokemon.stats['hp']
            hp_color = (50, 205, 50) if hp_ratio > 0.5 else (255, 140, 0) if hp_ratio > 0.2 else (220, 20, 60)
            
            hp_bar_rect = pygame.Rect(x-30, y+30, 100, 10)
            pygame.draw.rect(self.screen, (128, 128, 128), hp_bar_rect, border_radius=5)
            pygame.draw.rect(self.screen, hp_color, 
                            (hp_bar_rect.x, hp_bar_rect.y, hp_bar_rect.width * hp_ratio, hp_bar_rect.height),
                            border_radius=5)
        
        # 绘制治疗按钮
        heal_rect = pygame.Rect(
            self.screen_width//2 - 100,
            self.screen_height - 150,
            200, 50
        )
        self.buttons['heal'] = heal_rect  # 添加到按钮字典中
        pygame.draw.rect(self.screen, self.colors['button'], heal_rect, border_radius=5)
        heal_text = self.text_font.render("治疗全部宝可梦", True, (0, 0, 0))
        text_rect = heal_text.get_rect(center=heal_rect.center)
        self.screen.blit(heal_text, text_rect)
        
        # 添加返回按钮
        back_rect = pygame.Rect(10, self.screen_height - 60, 100, 40)
        self.buttons['back'] = back_rect
        pygame.draw.rect(self.screen, self.colors['button'], back_rect, border_radius=5)
        back_text = self.text_font.render("返回", True, (0, 0, 0))
        text_rect = back_text.get_rect(center=back_rect.center)
        self.screen.blit(back_text, text_rect)
    
    def _handle_shop_click(self, pos):
        """处理商店界面的点击"""
        current_player = self.game.get_current_player()
        
        # 检查按钮点击
        for button_id, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                # 播放按钮音效
                self.sound_manager.play_sound('button')
                
                # 处理返回按钮
                if button_id == 'back':
                    self._switch_to_next_player()
                    return
                
                # 处理购买按钮
                if button_id.startswith('buy_'):
                    item_id = button_id[4:]  # 移除 'buy_' 前缀
                    prices = {
                        'pokeball': 100,
                        'potion': 50,
                        'evolution_stone': 200
                    }
                    
                    if item_id in prices:
                        price = prices[item_id]
                        if current_player.money >= price:
                            current_player.money -= price
                            current_player.items[item_id] = current_player.items.get(item_id, 0) + 1
                            self.sound_manager.play_sound('button')
                            self._show_message(f"购买成功！剩余金钱：{current_player.money}", duration=1000)
                        else:
                            self._show_message("金钱不足！", duration=1000)
                        
                        # 重新绘制界面显示更新后的金钱
                        self.draw()
                        return
    
    def _handle_pokemon_center_click(self, pos):
        """处理宝可梦中心界面的点击"""
        if self.buttons.get('heal') and self.buttons['heal'].collidepoint(pos):
            # 获取进入宝可梦中心的玩家
            current_player = self.game.players[self.game.current_player]
            healed = False
            
            # 只恢复该玩家的宝可梦
            for pokemon in current_player.pokemon_list:
                if pokemon.current_hp < pokemon.stats['hp']:
                    pokemon.current_hp = pokemon.stats['hp']
                    healed = True
                # 恢复该宝可梦的所有技能PP
                for move in pokemon.moves:
                    if pokemon.current_pp[move['name']] < move['pp']:
                        pokemon.current_pp[move['name']] = move['pp']
                        healed = True
            
            if healed:
                # 播放治疗音效
                self.sound_manager.play_sound('heal')
                self._show_message("所有宝可梦已恢复！", duration=1000)
                # 重新绘制界面以显示更新后的状态
                self.draw()
                pygame.time.wait(500)  # 等待一小段时间让玩家看到效果
            else:
                self._show_message("所有宝可梦状态都很好！", duration=1000)
                self.draw()
                pygame.display.flip()
            
            # 无论是否治疗，都切换到游戏板并结束回合
            self._switch_to_next_player()
        
        # 检查返回按钮点击
        elif self.buttons.get('back') and self.buttons['back'].collidepoint(pos):
            # 直接切换到游戏板并结束回合
            self._switch_to_next_player()
    
    def _handle_dice_roll(self):
        """处理投骰子"""
        if not self.rolling_dice and not self.moving_player and self.can_roll_dice:
            self.rolling_dice = True
            self.dice_roll_start_time = pygame.time.get_ticks()
            self.dice_result = self.game.roll_dice()
            self.sound_manager.play_sound('dice')
            self.can_roll_dice = False  # 投完骰子后不能再投

    def draw_dice(self):
        """绘制骰子动画"""
        current_time = pygame.time.get_ticks()
        
        # 绘制上一次的骰子结果
        if self.last_dice_result is not None and not self.rolling_dice:
            dice_img = self.dice_frames[self.last_dice_result - 1]
            dice_rect = dice_img.get_rect(center=(self.screen_width//2, self.screen_height//2))
            self.screen.blit(dice_img, dice_rect)
            
            # 显示点数
            result_text = self.text_font.render(f"点数: {self.last_dice_result}", True, self.colors['text'])
            text_rect = result_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 50))
            self.screen.blit(result_text, text_rect)
        
        if self.rolling_dice:
            elapsed = current_time - self.dice_roll_start_time
            
            if elapsed < self.roll_duration:
                # 动画还在进行中
                frame_duration = 100  # 加快帧切换速度
                self.dice_frame_index = (elapsed // frame_duration) % len(self.dice_frames)
                dice_img = self.dice_frames[self.dice_frame_index]
                
                # 添加跳动效果
                bounce_height = math.sin(elapsed * 0.01) * 20
                dice_rect = dice_img.get_rect(center=(
                    self.screen_width//2,
                    self.screen_height//2 - bounce_height
                ))
                self.screen.blit(dice_img, dice_rect)
            else:
                # 动画结束，显示结果
                self.rolling_dice = False
                self.last_dice_result = self.dice_result
                self.start_player_movement()

    def start_player_movement(self):
        """开始玩家移动"""
        self.moving_player = True
        self.move_start_time = pygame.time.get_ticks()
        self.steps_left = self.dice_result
        self.step_duration = 300  # 每步移动时间（毫秒）

    def update_player_movement(self):
        """更新玩家移动动画"""
        if not self.moving_player:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.move_start_time
        
        if elapsed >= self.step_duration:
            current_player = self.game.get_current_player()
            
            # 移动一步
            if current_player.circle == 'outer':
                current_player.position = (current_player.position + 1) % len(self.game.outer_circle)
            else:
                current_player.position = (current_player.position + 1) % len(self.game.inner_circle)
            
            self.steps_left -= 1
            self.move_start_time = current_time
            
            # 检查是否完成移动
            if self.steps_left <= 0:
                self.moving_player = False
                event_result = self.game.handle_cell_event(current_player)
                if event_result:
                    self._handle_cell_event(event_result)
                else:
                    self._switch_to_next_player()  # 如果没有事件，直接切换到下一个玩家
    
    def draw_button(self, text, rect, state='normal'):
        """绘制美化的按钮"""
        # 绘制按钮背景
        button_img = self.button_images[state]
        scaled_button = pygame.transform.scale(button_img, rect.size)
        self.screen.blit(scaled_button, rect)
        
        # 绘制按钮文字
        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def draw_frame(self, frame_type, rect):
        """绘制美化的框架"""
        frame_img = self.frames[frame_type]
        scaled_frame = pygame.transform.scale(frame_img, rect.size)
        self.screen.blit(scaled_frame, rect)
    
    def _create_default_dice(self, number):
        """创建默认骰子图片"""
        size = (60, 60)
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255), surface.get_rect(), border_radius=10)
        text = self.text_font.render(str(number), True, (0, 0, 0))
        text_rect = text.get_rect(center=(size[0]//2, size[1]//2))
        surface.blit(text, text_rect)
        return surface
    
    def play_teleport_animation(self):
        """播放传送动画"""
        self.teleporting = True
        self.teleport_start_time = pygame.time.get_ticks()
        self.sound_manager.play_sound('teleport')
        
        # 获取家位置
        current_player = self.game.get_current_player()
        if current_player.circle == 'outer':
            pos = self.cell_positions['outer'][current_player.position]
        else:
            pos = self.cell_positions['inner'][current_player.position]
        
        # 添加传送动画
        self.animation_manager.add_animation('teleport', pos, duration=1000)
    
    def update_teleport_animation(self):
        """更新传送动画"""
        if not self.teleporting:
            return
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.teleport_start_time
        
        if elapsed >= self.teleport_duration:
            self.teleporting = False
            # 传送完成后自动切换玩家
            self._switch_to_next_player()
        else:
            # 绘制传送动画效果
            flash_interval = self.teleport_duration / (self.teleport_flash_count * 2)
            flash_on = (elapsed // flash_interval) % 2 == 0
            
            if flash_on:
                current_player = self.game.get_current_player()
                pos = self._get_player_position(current_player)
                pygame.draw.circle(self.screen, self.colors['teleport'],
                                 pos, 30, 3)
    
    def _draw_battle_messages(self, messages, area):
        """绘制消息"""
        if not messages:
            return
        
        # 创建消息框
        message_surface = pygame.Surface((area.width, area.height), pygame.SRCALPHA)
        pygame.draw.rect(message_surface, (255, 255, 255, 230), message_surface.get_rect(), border_radius=10)
        
        # 显示最后两条消息
        recent_messages = messages[-2:]
        for i, message in enumerate(recent_messages):
            text = self.text_font.render(message, True, (0, 0, 0))
            text_rect = text.get_rect(centerx=area.width//2, centery=area.height//2 + (i-0.5)*25)
            message_surface.blit(text, text_rect)
        
        # 显示消息框
        self.screen.blit(message_surface, area)
    
    def _show_battle_result(self, messages):
        """显示战斗结果"""
        if isinstance(messages, str):
            messages = [messages]
        
        # 创建结果显示界面
        result_surface = pygame.Surface((400, 300), pygame.SRCALPHA)
        pygame.draw.rect(result_surface, (255, 255, 255, 230), result_surface.get_rect(), border_radius=10)
        
        # 显示消息
        for i, message in enumerate(messages):
            text = self.text_font.render(message, True, (0, 0, 0))
            # 修复括号匹配问题
            text_rect = text.get_rect(centerx=200, y=30 + i * 30)
            result_surface.blit(text, text_rect)
        
        # 添加确认按钮
        button_rect = pygame.Rect(150, 250, 100, 40)
        pygame.draw.rect(result_surface, self.colors['button'], button_rect, border_radius=5)
        button_text = self.text_font.render("确定", True, (0, 0, 0))
        text_rect = button_text.get_rect(center=button_rect.center)
        result_surface.blit(button_text, text_rect)
        
        # 在屏幕中央显示结果
        result_rect = result_surface.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(result_surface, result_rect)
        pygame.display.flip()
        
        # 等待玩家点击确认
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # 转换为相对于result_surface的坐标
                    relative_pos = (
                        mouse_pos[0] - result_rect.x,
                        mouse_pos[1] - result_rect.y
                    )
                    if button_rect.collidepoint(relative_pos):
                        waiting = False
                        break
        
        # 返回游戏板并切换玩家
        self.current_state = 'game_board'
        self.game.next_player()
    
    def _create_default_pokemon_image(self, size, pokemon_id):
        """创建默认宝可梦图片"""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        
        # 确保 pokemon_id 是字符串
        pokemon_id = str(pokemon_id)
        
        # 根据宝可梦ID选择不同的颜色
        colors = {
            'pikachu': (255, 255, 0),      # 黄色
            'charmander': (255, 165, 0),   # 橙色
            'squirtle': (0, 191, 255),     # 蓝色
            'bulbasaur': (34, 139, 34),    # 绿色
            'eevee': (139, 69, 19),        # 棕色
            'meowth': (255, 215, 0),       # 金色
            'psyduck': (255, 215, 0),      # 金色
            'growlithe': (255, 140, 0)     # 橙色
        }
        color = colors.get(pokemon_id, (200, 200, 200))  # 默认灰色
        
        # 绘制一个圆形
        pygame.draw.circle(surface, color, (size[0]//2, size[1]//2), min(size[0], size[1])//2)
        
        # 添加文字标识（确保文字不超过4个字符）
        text = self.text_font.render(pokemon_id[:4] if len(pokemon_id) > 4 else pokemon_id, True, (0, 0, 0))
        text_rect = text.get_rect(center=(size[0]//2, size[1]//2))
        surface.blit(text, text_rect)
        
        return surface
    
    def _show_message(self, message, duration=1500):
        """显示消息"""
        # 创建消息框
        message_surface = pygame.Surface((400, 100), pygame.SRCALPHA)
        pygame.draw.rect(message_surface, (255, 255, 255, 230), message_surface.get_rect(), border_radius=10)
        
        # 渲染文本
        text = self.text_font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=(200, 50))
        message_surface.blit(text, text_rect)
        
        # 在屏幕中央显示消息
        message_rect = message_surface.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(message_surface, message_rect)
        pygame.display.flip()
        
        # 等待指定时间
        pygame.time.wait(duration)
    
    def draw_pokemon_list(self):
        """绘制当前玩家的宝可梦列表"""
        current_player = self.game.get_current_player()
        
        # 显示当前玩家信息
        player_text = self.text_font.render(f"{current_player.name}的宝可梦", True, (0, 0, 0))
        player_rect = player_text.get_rect(centerx=self.screen_width - 100, top=20)
        self.screen.blit(player_text, player_rect)
        
        # 创建宝可梦列表面板
        panel_width = 200
        panel_height = self.screen_height - 100
        panel_rect = pygame.Rect(
            self.screen_width - panel_width - 10,
            50,
            panel_width,
            panel_height
        )
        
        # 绘制半透明背景
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (255, 255, 200), panel_surface.get_rect(), border_radius=10)
        self.screen.blit(panel_surface, panel_rect)
        
        # 绘制标题
        title = self.text_font.render("我的宝可梦", True, (0, 0, 0))
        title_rect = title.get_rect(centerx=panel_rect.centerx, top=panel_rect.top + 10)
        self.screen.blit(title, title_rect)
        
        # 绘制宝可梦列表
        for i, pokemon in enumerate(current_player.pokemon_list):
            # 计�����置
            y = panel_rect.top + 50 + i * 90
            
            # 绘制宝可梦卡片背景
            card_rect = pygame.Rect(panel_rect.left + 10, y, panel_width - 20, 80)
            pygame.draw.rect(self.screen, (240, 240, 240), card_rect, border_radius=5)
            
            # 绘制宝可梦��片
            if pokemon.species in self.pokemon_images:
                image = self.pokemon_images[pokemon.species]['avatar']
            else:
                image = self._create_default_pokemon_image((32, 32), pokemon.species)
            
            image_rect = image.get_rect(left=card_rect.left + 10, centery=card_rect.centery)
            self.screen.blit(image, image_rect)
            
            # 绘制宝可梦信息
            info_text = [
                f"{pokemon.name} Lv.{pokemon.level}",
                f"HP: {pokemon.current_hp}/{pokemon.stats['hp']}"
            ]
            
            for j, text in enumerate(info_text):
                surface = self.text_font.render(text, True, (0, 0, 0))
                self.screen.blit(surface, (image_rect.right + 10, y + 20 + j * 20))
            
            # 绘制HP条
            hp_ratio = pokemon.current_hp / pokemon.stats['hp']
            hp_color = (50, 205, 50) if hp_ratio > 0.5 else (255, 140, 0) if hp_ratio > 0.2 else (220, 20, 60)
            
            hp_bar_rect = pygame.Rect(image_rect.right + 10, y + 60, 120, 8)
            pygame.draw.rect(self.screen, (128, 128, 128), hp_bar_rect, border_radius=4)
            if hp_ratio > 0:
                pygame.draw.rect(self.screen, hp_color,
                               (hp_bar_rect.left, hp_bar_rect.top,
                                hp_bar_rect.width * hp_ratio, hp_bar_rect.height),
                               border_radius=4)
        
        # 显示剩余空位
        remaining = Player.MAX_POKEMON - len(current_player.pokemon_list)
        if remaining > 0:
            text = self.text_font.render(f"剩余空位: {remaining}", True, (100, 100, 100))
            text_rect = text.get_rect(
                centerx=panel_rect.centerx,
                bottom=panel_rect.bottom - 10
            )
            self.screen.blit(text, text_rect)
    
    def _show_pokemon_management(self, new_pokemon):
        """显示宝可梦管理界面"""
        current_player = self.game.get_current_player()
        
        # 创建管理界面
        surface = pygame.Surface((600, 400), pygame.SRCALPHA)
        pygame.draw.rect(surface, (255, 255, 255, 230), surface.get_rect(), border_radius=10)
        
        # 显示提示信息
        text = self.text_font.render("队伍已满！请选择一只宝可梦替换或放新捕获的宝可梦", True, (0, 0, 0))
        text_rect = text.get_rect(centerx=300, top=20)
        surface.blit(text, text_rect)
        
        # 显示新捕获的宝可���
        self._draw_pokemon_card(surface, new_pokemon, (300, 80), True)
        
        # 显示现有宝可梦列表
        for i, pokemon in enumerate(current_player.pokemon_list):
            y = 160 + i * 90
            self._draw_pokemon_card(surface, pokemon, (300, y))
            
            # 添加替换按钮
            button_rect = pygame.Rect(420, y - 20, 80, 40)
            pygame.draw.rect(surface, self.colors['button'], button_rect, border_radius=5)
            button_text = self.text_font.render("替换", True, (0, 0, 0))
            text_rect = button_text.get_rect(center=button_rect.center)
            surface.blit(button_text, text_rect)
        
        # 添加放弃按钮
        cancel_rect = pygame.Rect(250, 350, 100, 40)
        pygame.draw.rect(surface, self.colors['button'], cancel_rect, border_radius=5)
        cancel_text = self.text_font.render("放弃", True, (0, 0, 0))
        text_rect = cancel_text.get_rect(center=cancel_rect.center)
        surface.blit(cancel_text, text_rect)
        
        # 在屏幕中央显示界面
        surface_rect = surface.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(surface, surface_rect)
        pygame.display.flip()
        
        # 等待玩家选择
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    relative_pos = (mouse_pos[0] - surface_rect.x, mouse_pos[1] - surface_rect.y)
                    
                    # 检查替换按钮点击
                    for i in range(len(current_player.pokemon_list)):
                        button_rect = pygame.Rect(420, 160 + i * 90 - 20, 80, 40)
                        if button_rect.collidepoint(relative_pos):
                            # 替换宝可梦
                            current_player.pokemon_list[i] = new_pokemon
                            self._show_battle_result([
                                "捕捉成功！",
                                f"使用{new_pokemon.name}替换了{current_player.pokemon_list[i].name}！"
                            ])
                            waiting = False
                            break
                        
                    # 检查放弃按��点击
                    if cancel_rect.collidepoint(relative_pos):
                        self._show_battle_result([
                            f"放弃了捕获{new_pokemon.name}！"
                        ])
                        waiting = False
    
    def _draw_pokemon_card(self, surface, pokemon, pos, is_new=False):
        """在固定��置上绘��宝可梦卡片"""
        x, y = pos
        
        # 绘制卡片背景
        card_rect = pygame.Rect(x - 80, y - 30, 160, 80)
        pygame.draw.rect(surface, (240, 240, 240) if not is_new else (255, 255, 200),
                        card_rect, border_radius=5)
        
        # 绘制宝可梦图片
        if pokemon.species in self.pokemon_images:
            image = self.pokemon_images[pokemon.species]['avatar']
        else:
            image = self._create_default_pokemon_image((32, 32), pokemon.species)
        
        image_rect = image.get_rect(left=x - 70, centery=y)
        surface.blit(image, image_rect)
        
        # 绘制宝可梦信息
        info_text = [
            f"{pokemon.name} Lv.{pokemon.level}",
            f"HP: {pokemon.current_hp}/{pokemon.stats['hp']}"
        ]
        
        for i, text in enumerate(info_text):
            text_surface = self.text_font.render(text, True, (0, 0, 0))
            surface.blit(text_surface, (x - 30, y - 20 + i * 20))
        
        # 绘制HP条
        hp_ratio = pokemon.current_hp / pokemon.stats['hp']
        hp_color = (50, 205, 50) if hp_ratio > 0.5 else (255, 140, 0) if hp_ratio > 0.2 else (220, 20, 60)
        
        hp_bar_rect = pygame.Rect(x - 30, y + 20, 100, 8)
        pygame.draw.rect(surface, (128, 128, 128), hp_bar_rect, border_radius=4)
        if hp_ratio > 0:
            pygame.draw.rect(surface, hp_color,
                            (hp_bar_rect.left, hp_bar_rect.top,
                             hp_bar_rect.width * hp_ratio, hp_bar_rect.height),
                            border_radius=4)
        
        # 如果是新捕获的宝可梦，添加新标识
        if is_new:
            new_text = self.text_font.render("新!", True, (255, 0, 0))
            surface.blit(new_text, (x + 60, y - 25))
    
    def _draw_pokemon(self, pokemon, pos, is_player):
        """在战斗界面绘制宝可梦"""
        x, y = pos
        
        # 获取宝可梦图片
        if pokemon.species in self.pokemon_images:
            image = self.pokemon_images[pokemon.species]['battle']
        else:
            image = self._create_default_pokemon_image((128, 128), pokemon.species)
        
        # 如果是敌方宝可梦，需要翻转图片
        if not is_player:
            image = pygame.transform.flip(image, True, False)
        
        # 绘制宝可梦
        image_rect = image.get_rect(center=pos)
        self.screen.blit(image, image_rect)
        
        # 绘制宝可梦信息
        info_text = [
            f"{pokemon.name} Lv.{pokemon.level}",
            f"HP: {pokemon.current_hp}/{pokemon.stats['hp']}"
        ]
        
        # 计算文本位置
        text_y = y - 80 if is_player else y - 100
        for i, text in enumerate(info_text):
            surface = self.text_font.render(text, True, (0, 0, 0))
            text_rect = surface.get_rect(center=(x, text_y + i * 25))
            self.screen.blit(surface, text_rect)
        
        # 绘制HP条
        hp_ratio = pokemon.current_hp / pokemon.stats['hp']
        hp_color = (50, 205, 50) if hp_ratio > 0.5 else (255, 140, 0) if hp_ratio > 0.2 else (220, 20, 60)
        
        hp_bar_width = 200
        hp_bar_height = 10
        hp_bar_rect = pygame.Rect(x - hp_bar_width//2, text_y + 50, hp_bar_width, hp_bar_height)
        
        # 绘制HP条背景
        pygame.draw.rect(self.screen, (128, 128, 128), hp_bar_rect, border_radius=5)
        
        # 绘制当前HP
        if hp_ratio > 0:
            current_hp_rect = pygame.Rect(
                hp_bar_rect.left,
                hp_bar_rect.top,
                hp_bar_width * hp_ratio,
                hp_bar_height
            )
            pygame.draw.rect(self.screen, hp_color, current_hp_rect, border_radius=5)
        
        # 如果是玩家的宝可梦，显示PP信息
        if is_player:
            # 在HP条下方显示每个技能的PP
            pp_y = text_y + 70
            for move in pokemon.moves:
                pp_text = f"{move['name']}: {pokemon.current_pp[move['name']]}/{move['pp']} PP"
                pp_surface = self.text_font.render(pp_text, True, (0, 0, 0))
                pp_rect = pp_surface.get_rect(center=(x, pp_y))
                self.screen.blit(pp_surface, pp_rect)
                pp_y += 20
    
    def _draw_hp_bar(self, pokemon, pos):
        """绘制HP条"""
        x, y = pos
        
        # 计算HP比例
        hp_ratio = pokemon.current_hp / pokemon.stats['hp']
        
        # 根据HP比例选择颜色
        if hp_ratio > 0.5:
            hp_color = (50, 205, 50)  # 绿色
        elif hp_ratio > 0.2:
            hp_color = (255, 140, 0)  # 橙色
        else:
            hp_color = (220, 20, 60)  # 红色
        
        # HP条的尺寸
        bar_width = 200
        bar_height = 10
        
        # 绘制HP条背景
        bg_rect = pygame.Rect(x - bar_width//2, y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (128, 128, 128), bg_rect, border_radius=5)
        
        # 绘制���前HP
        if hp_ratio > 0:
            current_width = int(bar_width * hp_ratio)
            current_rect = pygame.Rect(x - bar_width//2, y, current_width, bar_height)
            pygame.draw.rect(self.screen, hp_color, current_rect, border_radius=5)
        
        # 绘制HP数值
        hp_text = self.text_font.render(
            f"{pokemon.current_hp}/{pokemon.stats['hp']}", 
            True, 
            (0, 0, 0)
        )
        text_rect = hp_text.get_rect(
            centerx=x,
            top=y + bar_height + 5
        )
        self.screen.blit(hp_text, text_rect)
        
        # 绘制宝可梦名称和等级
        name_text = self.text_font.render(
            f"{pokemon.name} Lv.{pokemon.level}", 
            True, 
            (0, 0, 0)
        )
        name_rect = name_text.get_rect(
            centerx=x,
            bottom=y - 5
        )
        self.screen.blit(name_text, name_rect)
    
    def _draw_move_buttons(self, pokemon, area):
        """绘制技能按钮"""
        # 计算按钮大小和间距
        button_width = (area.width - 30) // 2
        button_height = (area.height - 10) // 2
        margin = 10
        
        for i, move in enumerate(pokemon.moves):
            # 计算按钮位置
            row = i // 2
            col = i % 2
            x = area.left + col * (button_width + margin)
            y = area.top + row * (button_height + margin)
            
            button_rect = pygame.Rect(x, y, button_width, button_height)
            
            # 检查PP是否足够
            move_name = move['name']
            has_pp = pokemon.current_pp[move_name] > 0  # 修复括号问题
            color = self.colors['button'] if has_pp else (200, 200, 200)
            text_color = (0, 0, 0) if has_pp else (128, 128, 128)
            
            # 绘制按钮
            pygame.draw.rect(self.screen, color, button_rect, border_radius=5)
            
            # 绘制技能名称
            move_text = self.text_font.render(move_name, True, text_color)
            text_rect = move_text.get_rect(centerx=button_rect.centerx, centery=button_rect.centery - 10)
            self.screen.blit(move_text, text_rect)
            
            # 绘制PP信息
            pp_text = self.text_font.render(f"PP: {pokemon.current_pp[move_name]}/{move['pp']}", True, text_color)
            pp_rect = pp_text.get_rect(centerx=button_rect.centerx, centery=button_rect.centery + 10)
            self.screen.blit(pp_text, pp_rect)
            
            # 添加到按钮字典
            self.buttons[f'move_{i}'] = button_rect
    
    def _draw_battle_action_buttons(self, battle, area):
        """绘制战斗功能按钮"""
        button_height = (area.height - 10) // 2
        
        # 绘制逃跑按钮
        escape_rect = pygame.Rect(area.left, area.top, area.width, button_height)
        pygame.draw.rect(self.screen, self.colors['button'], escape_rect, border_radius=5)
        escape_text = self.text_font.render("逃跑", True, (0, 0, 0))
        text_rect = escape_text.get_rect(center=escape_rect.center)
        self.screen.blit(escape_text, text_rect)
        self.buttons['escape'] = escape_rect
        
        # 如果是野生战斗，绘制捕捉按钮
        if battle.can_catch:
            catch_rect = pygame.Rect(area.left, area.top + button_height + 10, 
                                   area.width, button_height)
            pygame.draw.rect(self.screen, self.colors['button'], catch_rect, border_radius=5)
            catch_text = self.text_font.render("捕捉", True, (0, 0, 0))
            text_rect = catch_text.get_rect(center=catch_rect.center)
            self.screen.blit(catch_text, text_rect)
            self.buttons['catch'] = catch_rect
    
    def _handle_battle_click(self, pos):
        """处理战斗界面的点击"""
        battle = self.game.current_battle
        
        # 检查是否在战斗状态
        if not battle or battle.state != 'active':
            return
        
        # 检查按钮点击
        for button_id, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                # 播放按钮音效
                self.sound_manager.play_sound('button')
                
                if button_id == 'escape':
                    # 处理逃跑
                    result = battle.execute_turn('run')
                    if result and result.get('type') == 'battle_escaped':
                        self.sound_manager.play_sound('escape')
                        self._show_battle_result(["逃跑成功！"])
                        self.current_state = 'game_board'
                        self._switch_to_next_player()  # 使用统一的切换方法
                    else:
                        self._show_message("无法逃跑！")
                    return
                
                elif button_id == 'catch':
                    # 处理捕捉
                    result = battle.try_catch_pokemon()
                    if not result:
                        self._show_message("捕捉失败！")
                        return
                    
                    if result.get('type') == 'pokemon_escaped':
                        self.sound_manager.play_sound('escape')
                        self._show_battle_result([result.get('message', "宝可梦逃跑了！")])
                        self.current_state = 'game_board'
                        self._switch_to_next_player()  # 使用统一的切换方法
                        return
                    
                    # 播放捕捉音效和显示消息
                    self.sound_manager.play_sound('catch_start')
                    self._show_message("投掷精灵球...")
                    
                    if result.get('success'):
                        self.sound_manager.play_sound('catch_success')
                        current_player = battle.player  # 使用战斗对象中的玩家引用
                        if len(current_player.pokemon_list) >= Player.MAX_POKEMON:
                            self._show_pokemon_management(battle.enemy_pokemon)
                        else:
                            current_player.add_pokemon(battle.enemy_pokemon)
                            self._show_battle_result([
                                "捕捉成功！",
                                f"获得了{battle.enemy_pokemon.name}！"
                            ])
                        self.current_state = 'game_board'
                        self._switch_to_next_player()  # 使用统一的切换方法
                    else:
                        self.sound_manager.play_sound('catch_fail')
                        self._show_message(result.get('message', "捕捉失败！"))
                        # 捕捉失败不结束战斗，玩家可以继续选择其他行动
                    return
                
                elif button_id.startswith('move_'):
                    move_index = int(button_id.split('_')[1])
                    current_pokemon = self.game.get_current_player().pokemon_list[0]
                    
                    # 检查PP是否足够
                    move = current_pokemon.moves[move_index]
                    move_name = move['name']  # 先获取技能名称
                    current_pp = current_pokemon.current_pp[move_name]  # 再获取PP值
                    if current_pp <= 0:  # 最后进行比较
                        self._show_message("PP不足！")
                        return
                    
                    # 执行战斗回合
                    result = battle.execute_turn(move_index)
                    if result:
                        self.sound_manager.play_sound('attack')
                        self._handle_battle_result(result, current_pokemon)
                    return
    
    def _handle_battle_result(self, result, current_pokemon):
        """处理战斗结果"""
        result_type = result.get('type')
        
        if result_type in ['battle_won', 'battle_lost']:
            # 播放音效
            self.sound_manager.play_sound('victory' if result_type == 'battle_won' else 'defeat')
            
            # 准备消息
            messages = ["战斗胜利！" if result_type == 'battle_won' else "战斗失败..."]
            if result.get('exp_gained'):
                messages.append(f"获得了{result['exp_gained']}点经验值！")
            if result.get('level_up'):
                self.sound_manager.play_sound('level_up')
                messages.append(f"{current_pokemon.name}升级了！")
                messages.append(f"等级提升到{current_pokemon.level}！")
            
            # 显示结果并切换玩家
            self._show_battle_result(messages)
            self.end_turn()  # 使用统一的回合结束方法
        
        elif result_type == 'battle_continue':
            self.draw()
    
    def _load_resources(self):
        """加载游戏资源"""
        try:
            self._load_images()
            self._load_fonts()
            self._load_sounds()
            return True
        except Exception as e:
            print(f"资源加载错误: {str(e)}")
            return False
    
    def _load_images(self):
        """加载图片资源"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pokemon_dir = os.path.join(base_dir, 'assets', 'images', 'pokemon')
        self.pokemon_images = {}
        
        for pokemon_id in self.POKEMON_LIST:
            try:
                self.pokemon_images[pokemon_id] = {
                    'battle': self._load_image(pokemon_dir, f'{pokemon_id}_battle.png'),
                    'board': self._load_image(pokemon_dir, f'{pokemon_id}_board.png'),
                    'avatar': self._load_image(pokemon_dir, f'{pokemon_id}_avatar.png')
                }
                print(f"✓ 加载宝可梦图片: {pokemon_id}")
            except Exception as e:
                print(f"警告：{pokemon_id}图片加载失败 - {str(e)}")
                self.pokemon_images[pokemon_id] = self._create_default_pokemon_images(pokemon_id)

    def change_state(self, new_state):
        """切换游戏状态"""
        if new_state not in self.game_states:
            print(f"警告：无效的游戏状态 - {new_state}")
            return False
        
        # 执��状态退出逻辑
        self._exit_current_state()
        
        # 切换状态
        self.current_state = new_state
        
        # 执行新状态进入逻辑
        self._enter_new_state()
        return True

    def _exit_current_state(self):
        """退出当前状态时的清理工作"""
        if self.current_state == 'battle':
            self.game.current_battle = None
        self.buttons.clear()

    def _enter_new_state(self):
        """进入新状态时的初始化工作"""
        if self.current_state == 'game_board':
            self.sound_manager.play_music('game_background')
        elif self.current_state == 'battle':
            self.sound_manager.play_music('battle')

    def _handle_menu_click(self, pos):
        """处理主菜单界面的点击"""
        # 检查按钮点击
        for button_id, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                # 播放按钮音效
                self.sound_manager.play_sound('button')
                
                if button_id == 'start_game':
                    self.current_state = 'game_board'
                    self.sound_manager.play_music('game_background')
                elif button_id == 'load_game':
                    # TODO: 实现读取存档功能
                    pass
                elif button_id == 'settings':
                    # TODO: 实现设置界面
                    pass
                elif button_id == 'quit':
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    return

    def _handle_board_click(self, pos):
        """处理游戏板界面的点击"""
        # 检查是否在移动中
        if self.moving_player or self.rolling_dice:
            return
        
        # 检查是否是玩家的回合
        current_player = self.game.get_current_player()
        if not current_player:
            return
        
        # 检查骰子按钮点击
        dice_rect = pygame.Rect(
            self.screen_width//2 - 30,
            self.screen_height//2 - 30,
            60, 60
        )
        
        if dice_rect.collidepoint(pos):
            self._handle_dice_roll()
            return
        
        # 检查其他按钮点击
        for button_id, button_rect in self.buttons.items():
            if button_rect.collidepoint(pos):
                self.sound_manager.play_sound('button')
                self._handle_button_click(button_id)
                return

    def _switch_to_next_player(self):
        """切换到下一个玩家"""
        # 获取当前玩家编号（从0开始）
        current_player = self.game.current_player
        print(f"\n[切换玩家] 从玩家 {current_player + 1} 切换")
        
        # 重置所有状态
        self.rolling_dice = False
        self.moving_player = False
        self.steps_left = 0
        self.last_dice_result = None
        self.current_event = None
        self.game.current_battle = None  # 清除战斗状态
        
        # 切换玩家
        self.game.next_player()
        print(f"[切换玩家] 切换到玩家 {self.game.current_player + 1}")
        
        # 重置状态
        self.current_state = 'game_board'
        self.can_roll_dice = True
        
        # 显示新玩家回合提示
        self._show_message(f"玩家 {self.game.current_player + 1} 的回合", duration=1000)
        
        # 强制重绘界面
        self.draw()

    def update(self):
        """更新游戏状态"""
        current_time = pygame.time.get_ticks()
        
        if self.turn_state == TurnState.ROLLING:
            self._update_dice_animation(current_time)
        elif self.turn_state == TurnState.MOVING:
            self._update_movement(current_time)
        elif self.turn_state == TurnState.EVENT:
            self._update_event(current_time)

    def _update_dice_animation(self, current_time):
        """更新骰子动画"""
        if current_time - self.animation_timer >= self.animation_duration['roll']:
            self.rolling_dice = False
            self.turn_state = TurnState.MOVING
            self.start_player_movement()

    def _update_movement(self, current_time):
        """更新移动动画"""
        if not self.moving_player:
            return
            
        if current_time - self.animation_timer >= self.animation_duration['move']:
            self._move_one_step()
            self.animation_timer = current_time

    def _move_one_step(self):
        """移动一步"""
        current_player = self.game.get_current_player()
        
        # 移动玩家
        if current_player.circle == 'outer':
            current_player.position = (current_player.position + 1) % len(self.game.outer_circle)
        else:
            current_player.position = (current_player.position + 1) % len(self.game.inner_circle)
        
        self.steps_left -= 1
        
        # 检查是否完成移动
        if self.steps_left <= 0:
            self.moving_player = False
            self._check_cell_event()

    def _check_cell_event(self):
        """检查并处理格子事件"""
        current_player = self.game.get_current_player()
        event_result = self.game.handle_cell_event(current_player)
        
        if event_result:
            self.turn_state = TurnState.EVENT
            self.current_event = EventType[event_result['type'].upper()]
            self._start_event(event_result)
        else:
            self.end_turn()

    def _start_event(self, event_result):
        """开始处理事件"""
        if self.current_event == EventType.BATTLE:
            self._start_battle(event_result['enemy'])
        elif self.current_event == EventType.SHOP:
            self._start_shop()
        elif self.current_event == EventType.POKEMON_CENTER:
            self._start_pokemon_center()
        elif self.current_event == EventType.TELEPORT:
            self._start_teleport()
        else:
            self.end_turn()

    def _handle_shop_action(self, action):
        """处理商店操作"""
        if action == 'exit':
            self.end_turn()
        else:
            self._process_purchase(action)
            self.draw()

    def _handle_pokemon_center_action(self, action):
        """处理宝可梦中心操作"""
        if action == 'heal':
            self._heal_pokemon()
        self.end_turn()

    def can_roll_dice(self):
        """检查是否可以投骰子"""
        return (
            self.turn_state == TurnState.READY and 
            self.can_roll_dice and 
            not self.moving_player and 
            not self.rolling_dice
        )

    def can_handle_event(self):
        """检查是否可以处理事件"""
        return self.turn_state == TurnState.EVENT

    def start_turn(self):
        """开始新回合"""
        self.turn_state = TurnState.READY
        self.can_roll_dice = True
        self.rolling_dice = False
        self.moving_player = False
        self.steps_left = 0
        self.current_event = None
        self._show_message(f"玩家 {self.game.current_player + 1} 的回合", duration=1000)

    def end_turn(self):
        """结束当前回合"""
        # 重置所有状态
        self.rolling_dice = False
        self.moving_player = False
        self.steps_left = 0
        self.last_dice_result = None
        self.current_event = None
        self.game.current_battle = None  # 清除战斗状态
        
        # 切换玩家
        self.game.next_player()
        
        # 重置状态
        self.current_state = 'game_board'
        self.can_roll_dice = True
        
        # 显示新玩家回合提示
        self._show_message(f"玩家 {self.game.current_player + 1} 的回合", duration=1000)
        
        # 强制重绘界面
        self.draw()

    def _start_battle(self, event_result):
        """开始战斗"""
        self.current_state = 'battle'
        self.sound_manager.play_sound('battle_start')
        current_player = self.game.get_current_player()
        self.game.current_battle = Battle(
            self.game,
            current_player.pokemon_list[0],
            event_result['enemy']
        )

    def _start_shop(self):
        """进入商店"""
        self.current_state = 'shop'
        self.sound_manager.play_sound('button')

    def _start_pokemon_center(self):
        """进入宝可梦中心"""
        self.current_state = 'pokemon_center'
        self.sound_manager.play_sound('heal')

    def _handle_event_end(self, event_type, result=None):
        """处理事件结束"""
        if event_type == EventType.BATTLE:
            if result['type'] in ['battle_won', 'battle_lost']:
                self._show_battle_result(result)
                self.end_turn()
        elif event_type == EventType.SHOP:
            self.end_turn()
        elif event_type == EventType.POKEMON_CENTER:
            self.end_turn()
        elif event_type == EventType.TELEPORT:
            self.end_turn()

    def can_act(self):
        """检查当前是否可以行动"""
        return (
            self.turn_state == TurnState.READY and 
            not self.moving_player and 
            not self.rolling_dice and 
            self.can_roll_dice
        )

    def is_event_active(self):
        """检查是否正在处理事件"""
        return self.turn_state == TurnState.EVENT

    def _handle_cell_event(self, event_result):
        """处理格子事件"""
        event_type = event_result['type']
        current_player = self.game.get_current_player()
        
        if event_type == 'battle':
            self.current_state = 'battle'
            self.sound_manager.play_sound('battle_start')
            self.game.current_battle = Battle(
                self.game,
                current_player.pokemon_list[0],
                event_result['enemy']
            )
        elif event_type == 'shop':
            self.current_state = 'shop'
            self.sound_manager.play_sound('button')
        elif event_type == 'pokemon_center':
            self.current_state = 'pokemon_center'
            self.sound_manager.play_sound('heal')
        elif event_type == 'teleport':
            self.teleporting = True
            self.teleport_start_time = pygame.time.get_ticks()
            self.sound_manager.play_sound('teleport')
            # 执行传送
            if current_player.circle == 'outer':
                current_player.position = self.game.inner_teleport_pos
                current_player.circle = 'inner'
            else:
                current_player.position = self.game.outer_teleport_pos
                current_player.circle = 'outer'
            # 显示传送提示并结束回合
            self._show_message("传送！", duration=1000)
            pygame.time.wait(1000)
            self.end_turn()
        else:
            self.end_turn()