from includes.entity import *
from includes.ProgressBar import ProgressBar


class Game:
    ticks = 0
    secs = 0
    skillHold = 0

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.entityList = EntityList()

        # 创建角色实例
        roleImage = pygame.image.load("resource/role/zj.png")
        roleImage = pygame.transform.scale(roleImage, (roleImage.get_width() // 2, roleImage.get_height() // 2))
        roleX = screen.get_width() // 2 - roleImage.get_width() // 2
        roleY = screen.get_height() // 2 - roleImage.get_height() // 2
        self.role = Role(roleImage, roleX, roleY, screen, font)
        self.progress_bar = ProgressBar(screen, font, height=20, color=(255, 255, 255), progress_color=(0, 255, 0), textColor=(0,0,0))
        self.skillHoldBar = ProgressBar(screen, font, height=20, color=(255, 255, 255), progress_color=(0, 255, 0), textColor=(0,0,0))

        # 添加角色到实体列表
        self.entityList.addEntity(self.role)

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
            


    def addEntity(self,image,entityCls:Entity, x, y):
        entity = entityCls(image, x, y, self.screen, self.font)
        self.entityList.addEntity(entity)


    def update(self):
        self.ticks += 1
        self.secs == int(self.ticks/400)
        if self.ticks > 32767: self.tick = 0
        if not self.ticks%400:
            self.addEntity(None, ChestMonster, self.screen.get_width() // 2, self.screen.get_height() // 2)

        # update track
        for e in self.entityList.entities:
            if not e is self.role:
                e: Entity
                e.track(self.role.x, self.role.y)
        
        # monster progressbar
        self.progress_bar.setProgress(self.ticks%400/400)
        self.progress_bar.setText('刷怪倒计时')
        

        # 处理事件
        self.handleEvents()

        # 获取按键状态
        keys = pygame.key.get_pressed()
        hold = False
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.skillHold += 5
            hold = True
        if not hold and not self.skillHold < 0: self.skillHold -= 10
        if self.skillHold < 0: self.skillHold = 0

        # update pull
        if keys[pygame.K_SPACE]:
            for e in self.entityList.entities:
                if not e is self.role:
                    e: Entity
                    e.pull(self.role.x, self.role.y, 10)

        # update player skill
        if self.skillHold > 4000:
            while len(self.entityList.entities) > 1:
                e = self.entityList.entities.pop()
                if not e is self.role:
                    del e
                else:
                    self.entityList.addEntity(e)

        # 更新角色位置
        self.role.updatePosition(keys, self.screen.get_width(), self.screen.get_height())

        # 绘制背景
        self.screen.fill((255,0,0))

        # draw progressbar
        self.progress_bar.draw()
        if self.skillHold > 0:
            self.skillHoldBar.setProgress(self.skillHold/4000)
            self.skillHoldBar.draw((self.screen.get_width() - self.skillHoldBar.width) // 2, y = self.screen.get_height() - (self.skillHoldBar.height*2) - 20)

        # 绘制实体列表中的所有实体
        self.entityList.drawEntities(self.screen)

        # draw position
        # self.role.drawPosition()
        
        # draw ticks
        # self.drawText(self.screen.get_width()/2, 200, str(int(self.ticks/400)), (255,255,255))

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