from PIL import Image
import os

def process_pikachu():
    # 确保输出目录存在
    output_dir = 'assets/images/pokemon'
    os.makedirs(output_dir, exist_ok=True)
    
    # 加载原图
    img = Image.open('pikachu.png')  # 确保皮卡丘图片在当前目录
    img = img.convert('RGBA')
    
    # 处理三种尺寸
    sizes = {
        'battle': (128, 128),
        'board': (64, 64),
        'avatar': (32, 32)
    }
    
    for name, size in sizes.items():
        # 创建新的透明背景图像
        new_img = Image.new('RGBA', size, (0, 0, 0, 0))
        
        # 等比例缩放
        img_copy = img.copy()
        img_copy.thumbnail(size, Image.Resampling.LANCZOS)
        
        # 计算居中位置
        x = (size[0] - img_copy.width) // 2
        y = (size[1] - img_copy.height) // 2
        
        # 粘贴到新图像上
        new_img.paste(img_copy, (x, y), img_copy)
        
        # 保存
        output_path = os.path.join(output_dir, f'pikachu_{name}.png')
        new_img.save(output_path, 'PNG')
        print(f"✓ 已保存: {output_path}")

if __name__ == "__main__":
    process_pikachu() 