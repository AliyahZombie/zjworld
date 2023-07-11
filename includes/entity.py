import pygame
from pygame import Surface
from pygame.font import Font

def drawText(screen, font, x, y, text='', color=(255,0,0)):
    # 得到角色坐标的文本对象
    coordText = font.render(text, True, color)
    # 绘制角色坐标文本
    textRect = coordText.get_rect()
    textRect.center = (x, y)
    screen.blit(coordText, textRect)

# 实体类
class Entity:
    def __init__(self, image:Surface, x:float, y:float, screen:Surface, font:Font):
        self.image = image
        self.x = x
        self.y = y
        self.screen = screen
        self.font = font

    def draw(self, screen:Surface):
        screen.blit(self.image, (self.x, self.y))

class Role(Entity):
    step = 0.03
    def __init__(self, image:Surface, x:float, y:float,screen:Surface, font:Font):
        super().__init__(image, x, y,screen, font)
        self.vx, self.vy = 0, 0 # 速度
        self.ax, self.ay = 0, 0 # 加速度
    
    def drawPosition(self):
        drawText(self.screen, self.font,self.x + self.image.get_width() // 2, self.y + 20, f"Current position: ({self.x}, {self.y})")
        

    def updatePosition(self, keys, step, screenWidth, screenHeight):
        # 计算加速度
        self.ax, self.ay = 0, 0
        if keys[pygame.K_w] and self.y > 0:
            self.ay = -self.step
        if keys[pygame.K_s] and self.y < screenHeight - self.image.get_height():
            self.ay = self.step
        if keys[pygame.K_a] and self.x > 0:
            self.ax = -self.step
        if keys[pygame.K_d] and self.x < screenWidth - self.image.get_width():
            self.ax = self.step
        
        # 计算速度和位置
        self.vx += self.ax
        self.vy += self.ay
        new_x = self.x + self.vx
        new_y = self.y + self.vy
        
        # 检查角色是否会跑出屏幕
        if new_x < 0:
            new_x = 0
            self.vx = 0
        elif new_x > screenWidth - self.image.get_width():
            new_x = screenWidth - self.image.get_width()
            self.vx = 0
        if new_y < 0:
            new_y = 0
            self.vy = 0
        elif new_y > screenHeight - self.image.get_height():
            new_y = screenHeight - self.image.get_height()
            self.vy = 0
        
        self.x, self.y = new_x, new_y
        
        # 加入摩擦力，让速度逐渐减小
        self.vx *= 0.99
        self.vy *= 0.99

# 实体列表类
class EntityList:
    def __init__(self):
        self.entities = []

    def addEntity(self, entity):
        self.entities.append(entity)

    def drawEntities(self, screen):
        for entity in self.entities:
            entity.draw(screen)