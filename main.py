import pygame
import os
from includes.entity import Entity, Role, EntityList, drawText
import random
from includes.game import Game


# 初始化Pygame
pygame.init()

# 加载中文字体文件
fontPath = "resource/font/wryh.ttc"
if not os.path.isfile(fontPath):
    raise FileNotFoundError(f"Font file '{fontPath}' not found.")

# 创建字体对象
font = pygame.font.Font(fontPath, 24)

# 创建窗口
screenFlags = pygame.FULLSCREEN
screen = pygame.display.set_mode((0, 0), screenFlags)

# 创建游戏对象
game = Game(screen, font)

# 游戏主循环
while True:
    game.update()

# 退出游戏
pygame.quit()