import pygame
from pygame import Surface
from pygame.font import Font
import math

def drawText(screen, font, x, y, text='', color=(255,0,0)):
    # 得到角色坐标的文本对象
    coordText = font.render(text, True, color)
    # 绘制角色坐标文本
    textRect = coordText.get_rect()
    textRect.center = (x, y)
    screen.blit(coordText, textRect)

# 实体类
class Entity:
    def __init__(self, image: Surface, x: float, y: float, screen: Surface, font: Font):
        self.image = image
        self.x = x
        self.y = y
        self.screen = screen
        self.font = font
        self.motion = [0.0, 0.0]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen: Surface):
        self.x += self.motion[0]
        self.y += self.motion[1]
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, (self.x, self.y))
    
    def drawPosition(self):
        drawText(self.screen, self.font, self.x + self.image.get_width() // 2, self.y + 20, f"Current position: ({self.x}, {self.y})")
        
    def applyFriction(self, friction: float):
        self.motion[0] *= friction
        self.motion[1] *= friction
        if abs(self.motion[0]) < 0.1:
            self.motion[0] = 0.0
        if abs(self.motion[1]) < 0.1:
            self.motion[1] = 0.0
            
    def track(self, target_x: float, target_y: float, step: float = 1.0):
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        length = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if length == 0:
            return
        direction_x = delta_x / length
        direction_y = delta_y / length
        self.motion[0] = direction_x * step
        self.motion[1] = direction_y * step
    
    def resolveCollision(self, other: 'Entity'):
        # Calculate the displacement vector between the two entities
        delta_x = self.rect.centerx - other.rect.centerx
        delta_y = self.rect.centery - other.rect.centery
        
        # Check if the entities are overlapping exactly
        if delta_x == 0 and delta_y == 0:
            delta_x = 1
            
        # Calculate the minimum displacement needed to separate the two entities
        min_distance = self.rect.width / 2 + other.rect.width / 2
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        separation_x = delta_x / distance * (min_distance - distance)
        separation_y = delta_y / distance * (min_distance - distance)
        
        # Move the entities to their separated positions
        self.x += separation_x / 2
        self.y += separation_y / 2
        other.x -= separation_x / 2
        other.y -= separation_y / 2
        self.rect.x = self.x
        self.rect.y = self.y
        other.rect.x = other.x
        other.rect.y = other.y
    
    def pull(self, target_x: float, target_y: float, step: float):
        delta_x = self.x - target_x
        delta_y = self.y - target_y
        distance = max(math.sqrt(delta_x ** 2 + delta_y ** 2), 1.0)
        direction_x = delta_x / distance
        direction_y = delta_y / distance

        # Calculate screen boundaries
        left_bound = self.rect.width // 2
        right_bound = self.screen.get_width() - self.rect.width // 2
        top_bound = self.rect.height // 2
        bottom_bound = self.screen.get_height() - self.rect.height // 2

        # Check if entity will be pushed out of screen
        new_x = self.x + direction_x * step
        new_y = self.y + direction_y * step
        if new_x < left_bound or new_x > right_bound or new_y < top_bound or new_y > bottom_bound:
            self.motion[0] = 0.0
            self.motion[1] = 0.0
        else:
            self.motion[0] = direction_x * step
            self.motion[1] = direction_y * step

class ChestMonster(Entity):
    def __init__(self, image, x: float, y: float, screen: Surface, font: Font):
        image = pygame.image.load('resource/entity/chest.png')
        # image = pygame.transform.scale(image, (image.get_width()*5, image.get_height()*5))
        super().__init__(image, x, y, screen, font)
        self.motion = [2,2]


class Role(Entity):
    step = 1.5
    def __init__(self, image:Surface, x:float, y:float,screen:Surface, font:Font):
        super().__init__(image, x, y,screen, font)
    
    def updatePosition(self, keys, screenWidth, screenHeight):
        # 直接设置瞬时移动速度
        x_motion, y_motion = self.motion
        if keys[pygame.K_w] and self.y > 0:
            y_motion = -self.step
        if keys[pygame.K_s] and self.y < screenHeight - self.image.get_height():
            y_motion = self.step
        if keys[pygame.K_a] and self.x > 0:
            x_motion = -self.step
        if keys[pygame.K_d] and self.x < screenWidth - self.image.get_width():
            x_motion = self.step
        self.motion = [x_motion, y_motion]
        
        # 更新实体的位置
        self.x += x_motion
        self.y += y_motion
        
        # 检查角色是否会跑出屏幕
        if self.x < 0:
            self.x = 0
        elif self.x > screenWidth - self.image.get_width():
            self.x = screenWidth - self.image.get_width()
        
        if self.y < 0:
            self.y = 0
        elif self.y > screenHeight - self.image.get_height():
            self.y = screenHeight - self.image.get_height()
        
        # 应用摩擦力
        self.applyFriction(0.99)


# 实体列表类
class EntityList:
    def __init__(self):
        self.entities = []
    
    def addEntity(self, entity: Entity):
        self.entities.append(entity)
    
    def drawEntities(self, screen: Surface):
        self.screen = screen
        self.update()
        return
        for entity in self.entities:
            entity.draw(screen)
    
    def detectCollisions(self):
        for i in range(len(self.entities)):
            for j in range(i+1, len(self.entities)):
                entity1 = self.entities[i]
                entity2 = self.entities[j]
                if entity1.rect.colliderect(entity2.rect):
                    entity1.resolveCollision(entity2)
    
    def update(self):
        self.detectCollisions()
        for entity in self.entities:
            entity.applyFriction(0.95)
            entity.draw(self.screen)