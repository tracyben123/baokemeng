# 图片资源说明

## 目录结构
- pokemon/: 宝可梦图片
  - source/: 原始图片
  - *.png: 处理后的图片
- ui/: 界面元素
  - buttons/: 按钮
  - frames/: 框架
  - icons/: 图标
- board/: 棋盘相关
- dice/: 骰子图片

## 命名规范
- 宝可梦图片：`{pokemon_name}_{usage}.png`
  - usage: battle/board/avatar
- UI元素：`{type}_{state}.png`
  - type: button/frame/icon
  - state: normal/hover/pressed 