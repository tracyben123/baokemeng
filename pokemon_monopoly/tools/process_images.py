import os
import sys
from PIL import Image
import pygame

def process_pokemon_images():
    """处理宝可梦图片"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_dir = os.path.join(base_dir, 'raw_assets', 'images', 'pokemon')
    output_dir = os.path.join(base_dir, 'assets', 'images', 'pokemon')
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'source'), exist_ok=True)
    
    # 定义需要处理的宝可梦列表
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
    
    # 定义不同用途的尺寸
    sizes = {
        'battle': (256, 256),  # 战斗时使用大图
        'board': (64, 64),     # 棋盘上使用中等图
        'avatar': (32, 32)     # 状态栏使用小图
    }
    
    # 处理每个宝可梦的图片
    for pokemon_id in pokemon_list:
        # 首先复制原始图片到source目录
        raw_path = os.path.join(source_dir, f'{pokemon_id}.png')
        source_path = os.path.join(output_dir, 'source', f'{pokemon_id}.png')
        
        if os.path.exists(raw_path):
            print(f"处理 {pokemon_id} 的图片...")
            try:
                # 复制原始图片
                import shutil
                shutil.copy2(raw_path, source_path)
                
                with Image.open(raw_path) as img:
                    # 确保图片有透明通道
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    # 为每个用途生成对应尺寸的图片
                    for usage, size in sizes.items():
                        # 保持纵横比的缩放
                        img_ratio = img.width / img.height
                        if img_ratio > 1:
                            new_width = size[0]
                            new_height = int(size[0] / img_ratio)
                        else:
                            new_height = size[1]
                            new_width = int(size[1] * img_ratio)
                        
                        # 创建新的透明背景
                        new_img = Image.new('RGBA', size, (0, 0, 0, 0))
                        
                        # 缩放原图
                        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        
                        # 将缩放后的图片粘贴到中心位置
                        paste_x = (size[0] - new_width) // 2
                        paste_y = (size[1] - new_height) // 2
                        new_img.paste(resized, (paste_x, paste_y), resized)
                        
                        # 保存处理后的图片
                        output_path = os.path.join(output_dir, f'{pokemon_id}_{usage}.png')
                        new_img.save(output_path, 'PNG')
                        
                print(f"✓ {pokemon_id} 处理完成")
            except Exception as e:
                print(f"× {pokemon_id} 处理失败: {str(e)}")
        else:
            print(f"× 未找到 {pokemon_id} 的源图片: {raw_path}")

def process_ui_images():
    """处理UI图片"""
    source_dir = os.path.join('assets', 'images', 'ui', 'source')
    output_dir = os.path.join('assets', 'images', 'ui')
    
    # 处理按钮
    button_sizes = {
        'normal': (200, 50),
        'small': (100, 30)
    }
    
    for filename in os.listdir(os.path.join(source_dir, 'buttons')):
        if filename.endswith(('.png', '.jpg')):
            with Image.open(os.path.join(source_dir, 'buttons', filename)) as img:
                for size_name, size in button_sizes.items():
                    resized = img.resize(size, Image.Resampling.LANCZOS)
                    output_path = os.path.join(output_dir, 'buttons', f"{size_name}_{filename}")
                    resized.save(output_path, 'PNG')

def process_effect_images():
    """处理特效图片"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    effects_dir = os.path.join(base_dir, 'assets', 'images', 'effects')
    
    # 确保特效目录存在
    for effect_type in ['attack', 'heal', 'evolution', 'catch', 'teleport']:
        effect_dir = os.path.join(effects_dir, effect_type)
        os.makedirs(effect_dir, exist_ok=True)
        
        # 生成特效帧
        for i in range(1, 7):
            size = 64
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # 为不同特效类型选择不同颜色
            colors = {
                'attack': (255, 0, 0),      # 红色
                'heal': (0, 255, 0),        # 绿色
                'evolution': (255, 255, 0),  # 黄色
                'catch': (0, 0, 255),       # 蓝色
                'teleport': (255, 165, 0)   # 橙色
            }
            color = colors[effect_type]
            
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
            output_path = os.path.join(effect_dir, f'frame_{i}.png')
            pygame.image.save(surface, output_path)
        
        print(f"✓ {effect_type} 特效生成完成")

def main():
    """主函数"""
    print("开始处理图片资源...")
    
    try:
        process_pokemon_images()
        print("✓ 宝可梦图片处理完成")
        
        process_ui_images()
        print("✓ UI图片处理完成")
        
        process_effect_images()
        print("✓ 特效图片处理完成")
        
    except Exception as e:
        print(f"错误：图片处理失败 - {str(e)}")
        sys.exit(1)
    
    print("所有图片处理完成！")

if __name__ == "__main__":
    main()