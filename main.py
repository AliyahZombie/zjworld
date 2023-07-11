import pygame
import os

# 实体类
class Entity:
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 角色类
class Role(Entity):
    def __init__(self, image, x, y):
        super().__init__(image, x, y)

    def updatePosition(self, keys, step, screenWidth, screenHeight):
        if keys[pygame.K_w] and self.y > 0:
            self.y -= step
        if keys[pygame.K_s] and self.y < screenHeight - self.image.get_height():
            self.y += step
        if keys[pygame.K_a] and self.x > 0:
            self.x -= step
        if keys[pygame.K_d] and self.x < screenWidth - self.image.get_width():
            self.x += step

# 实体列表类
class EntityList:
    def __init__(self):
        self.entities = []

    def addEntity(self, entity):
        self.entities.append(entity)

    def drawEntities(self, screen):
        for entity in self.entities:
            entity.draw(screen)


# 初始化Pygame
pygame.init()

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
role = Role(roleImage, roleX, roleY)

# 创建实体列表并添加角色
entityList = EntityList()
entityList.addEntity(role)

# 移动步长
step = 0.5

# 加载中文字体文件
fontPath = "resource/font/wryh.ttc"
if not os.path.isfile(fontPath):
    raise FileNotFoundError(f"Font file '{fontPath}' not found.")

# 创建字体对象
font = pygame.font.Font(fontPath, 24)

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
    screen.fill((255, 255, 255))

    # 绘制实体列表中的所有实体
    entityList.drawEntities(screen)

    # 得到角色坐标的文本对象
    coordText = font.render(f"Current position: ({role.x}, {role.y})", True, (255, 0, 0))

    # 绘制角色坐标文本
    textRect = coordText.get_rect()
    textRect.center = (role.x + role.image.get_width() // 2, role.y + 20)
    screen.blit(coordText, textRect)

    # 更新屏幕
    pygame.display.flip()

# 退出游戏
pygame.quit()