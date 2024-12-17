import pygame
import os

def test_fonts():
    pygame.init()
    
    # 创建一个测试窗口
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('字体测试')
    
    font_files = {
        'Bold': 'assets/fonts/SourceHanSansSC-Bold.otf',
        'Regular': 'assets/fonts/SourceHanSansSC-Regular.otf'
    }
    
    results = []
    
    # 测试每个字体文件
    for font_name, font_path in font_files.items():
        try:
            # 检查文件是否存在
            if not os.path.exists(font_path):
                results.append(f"{font_name}: 文件不存在 ({font_path})")
                continue
                
            # 尝试加载字体
            font = pygame.font.Font(font_path, 32)
            
            # 尝试渲染中文文本
            text = font.render('测试文本：宝可梦大富翁', True, (0, 0, 0))
            
            results.append(f"{font_name}: 加载成功")
            
        except Exception as e:
            results.append(f"{font_name}: 加载失败 - {str(e)}")
    
    # 打印测试结果
    print("\n=== 字体测��结果 ===")
    for result in results:
        print(result)
    
    # 显示测试结果
    screen.fill((255, 255, 255))
    y = 50
    for font_name, font_path in font_files.items():
        try:
            font = pygame.font.Font(font_path, 32)
            text = font.render(f'使用 {font_name} 字体：宝可梦大富翁', True, (0, 0, 0))
            screen.blit(text, (50, y))
            y += 50
        except:
            pass
    
    pygame.display.flip()
    
    # 等待用户关闭窗口
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()

if __name__ == '__main__':
    test_fonts() 