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
        self.motion = [0.0, 0.0]  # 初始化瞬时移动速度为0
    
    def draw(self, screen:Surface):
        # 更新坐标
        self.x += self.motion[0]
        self.y += self.motion[1]
        
        # 绘制实体
        screen.blit(self.image, (self.x, self.y))
    
    def drawPosition(self):
        drawText(self.screen, self.font, self.x + self.image.get_width() // 2, self.y + 20, f"Current position: ({self.x}, {self.y})")
        
    def applyFriction(self, friction:float):
        # 乘以摩擦系数以逐渐减小瞬时移动速度
        self.motion[0] *= friction
        self.motion[1] *= friction
        # 当瞬时移动速度到一定小时归零，以避免出现微小的移动
        if abs(self.motion[0]) < 0.1:
            self.motion[0] = 0.0
        if abs(self.motion[1]) < 0.1:
            self.motion[1] = 0.0


class Role(Entity):
    step = 0.5
    def __init__(self, image:Surface, x:float, y:float,screen:Surface, font:Font):
        super().__init__(image, x, y,screen, font)
    
    def updatePosition(self, keys, screenWidth, screenHeight):
        # 计算加速度
        ax, ay = 0, 0
        if keys[pygame.K_w] and self.y > 0:
            ay = -self.step
        if keys[pygame.K_s] and self.y < screenHeight - self.image.get_height():
            ay = self.step
        if keys[pygame.K_a] and self.x > 0:
            ax = -self.step
        if keys[pygame.K_d] and self.x < screenWidth - self.image.get_width():
            ax = self.step
        
        # 更新实体的瞬时移动速度
        self.motion[0] += ax
        self.motion[1] += ay
        
        # 检查角色是否会跑出屏幕
        if self.x + self.motion[0] < 0:
            self.motion[0] = -self.motion[0]
            self.x = 0
        elif self.x + self.motion[0] > screenWidth - self.image.get_width():
            self.motion[0] = -self.motion[0]
            self.x = screenWidth - self.image.get_width()
        else:
            self.x += self.motion[0]
        
        if self.y + self.motion[1] < 0:
            self.motion[1] = -self.motion[1]
            self.y = 0
        elif self.y + self.motion[1] > screenHeight - self.image.get_height():
            self.motion[1] = -self.motion[1]
            self.y = screenHeight - self.image.get_height()
        else:
            self.y += self.motion[1]
        
        # 应用摩擦力
        self.applyFriction(0.99)


# 实体列表类
class EntityList:
    def __init__(self):
        self.entities = []

    def addEntity(self, entity):
        self.entities.append(entity)

    def drawEntities(self, screen):
        for entity in self.entities:
            entity.draw(screen)