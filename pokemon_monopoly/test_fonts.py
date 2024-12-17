import os
import pygame

def check_fonts():
    font_paths = [
        'assets/fonts/SourceHanSansSC-Bold.otf',
        'assets/fonts/SourceHanSansSC-Regular.otf'
    ]
    
    print("\n=== 检查字体文件 ===")
    for path in font_paths:
        if os.path.exists(path):
            print(f"✓ {path} 存在")
        else:
            print(f"✗ {path} 不存在")
            
    return all(os.path.exists(path) for path in font_paths)

def test_font_rendering():
    import pygame
    pygame.init()
    
    print("\n=== 测试字体渲染 ===")
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("字体测试")
    
    try:
        # 测试 Regular 字体
        regular_font = pygame.font.Font('assets/fonts/SourceHanSansSC-Regular.otf', 32)
        regular_text = regular_font.render("Regular字体测试：宝可梦", True, (0, 0, 0))
        print("✓ Regular 字体加载成功")
        
        # 测试 Bold 字体
        bold_font = pygame.font.Font('assets/fonts/SourceHanSansSC-Bold.otf', 32)
        bold_text = bold_font.render("Bold字体测试：宝可梦", True, (0, 0, 0))
        print("✓ Bold 字体加载成功")
        
        # 显示测试结果
        screen.fill((255, 255, 255))
        screen.blit(regular_text, (50, 100))
        screen.blit(bold_text, (50, 200))
        pygame.display.flip()
        
        print("\n请查看弹出的窗口，确认文字显示是否正常")
        print("按关闭按钮退出测试")
        
        # 等待用户关闭窗口
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
    except Exception as e:
        print(f"✗ 字体测试失败: {str(e)}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    if check_fonts():
        test_font_rendering()
    else:
        print("\n请确保字体文件已正确放置在 assets/fonts/ 目录下") 