from includes.entity import *


class Game:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.entityList = EntityList()
        self.ticks = 0

        # 创建角色实例
        roleImage = pygame.image.load("resource/role/zj.png")
        roleImage = pygame.transform.scale(roleImage, (roleImage.get_width() // 2, roleImage.get_height() // 2))
        roleX = screen.get_width() // 2 - roleImage.get_width() // 2
        roleY = screen.get_height() // 2 - roleImage.get_height() // 2
        self.role = Role(roleImage, roleX, roleY, screen, font)

        # 添加角色到实体列表
        self.entityList.addEntity(self.role)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def update(self):
        self.ticks += 1
        if self.ticks > 32767: self.tick = 0
        # 处理事件
        self.handleEvents()

        # 获取按键状态
        keys = pygame.key.get_pressed()

        # 更新角色位置
        self.role.updatePosition(keys, self.screen.get_width(), self.screen.get_height())

        # 绘制背景
        self.screen.fill((0, 0, 0))

        # 绘制实体列表中的所有实体
        self.entityList.drawEntities(self.screen)

        # draw position
        self.role.drawPosition()
        
        # draw ticks
        self.drawText(self.screen.get_width()/2, 200, str(self.ticks), (0,0,0))

        # 更新屏幕
        pygame.display.flip()
    
    def drawText(self, x, y, text='', color=(255,0,0)):
        # 得到角色坐标的文本对象
        coordText = self.font.render(text, True, color)
        # 绘制角色坐标文本
        textRect = coordText.get_rect()
        textRect.center = (x, y)
        self.screen.blit(coordText, textRect)
    
    def quit(self):
        # 退出游戏
        pygame.quit()
        quit()