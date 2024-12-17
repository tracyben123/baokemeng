import pygame
from game import Game
from gui import MinimalGUI

def main():
    # 初始化游戏
    game = Game()
    gui = MinimalGUI(game)
    
    # 游戏主循环
    running = True
    clock = pygame.time.Clock()
    
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                gui.handle_event(event)
        
        # 绘制界面
        gui.draw()
        
        # 控制帧率
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()