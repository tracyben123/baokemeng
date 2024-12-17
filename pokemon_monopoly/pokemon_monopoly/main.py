import pygame
from .game import Game
from .gui import MinimalGUI

def main():
    # 初始化游戏
    pygame.init()
    game = Game()
    gui = MinimalGUI(game)
    
    # 主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 只有在鼠标左键点击时才处理
                if event.button == 1:  # 左键点击
                    gui.handle_event(event)
            elif event.type == pygame.KEYDOWN:
                gui.handle_event(event)
        
        # 更新显示
        gui.draw()
        
        # 控制帧率
        pygame.time.Clock().tick(60)
    
    # 退出游戏
    pygame.quit()

if __name__ == "__main__":
    main() 