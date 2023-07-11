import pygame
import os
from includes.entity import Entity,Role,EntityList,drawText
import random


# 初始化Pygame
pygame.init()

# 加载中文字体文件
fontPath = "resource/font/wryh.ttc"
if not os.path.isfile(fontPath):
    raise FileNotFoundError(f"Font file '{fontPath}' not found.")

# 创建字体对象
font = pygame.font.Font(fontPath, 24)
# 询问玩家是否开启全屏
fullscreen = input("Do you want to enable fullscreen mode? (y/n): ")
screenFlags = pygame.FULLSCREEN if fullscreen.lower() == "y" else 0

# 创建窗口
screen = pygame.display.set_mode((0, 0), screenFlags)

# 创建角色实例
roleImage = pygame.image.load("resource/role/zj.png")
roleImage = pygame.transform.scale(roleImage, (roleImage.get_width() // 2, roleImage.get_height() // 2))
roleX = screen.get_width() // 2 - roleImage.get_width() // 2
roleY = screen.get_height() // 2 - roleImage.get_height() // 2
role = Role(roleImage, roleX, roleY,screen, font)

# 创建实体列表并添加角色
entityList = EntityList()
entityList.addEntity(role)

# 移动步长
step = 0.5


# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # 获取按键状态
    keys = pygame.key.get_pressed()

    # 更新角色位置
    role.updatePosition(keys, step, screen.get_width(), screen.get_height())

    # 绘制背景
    #screen.fill( (random.randint(0,255), random.randint(0,255),random.randint(0,255)) )
    screen.fill((255,255,255))

    # 绘制实体列表中的所有实体
    entityList.drawEntities(screen)

    # draw position
    role.drawPosition()

    # 更新屏幕
    pygame.display.flip()

# 退出游戏
pygame.quit()