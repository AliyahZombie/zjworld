import pygame

class ProgressBar:
    def __init__(self, screen, font, height=40, width=None, color=(255, 255, 255), progress_color=(0, 255, 0),textColor=(255,255,255)):
        self.screen = screen
        self.font = font
        self.height = height
        if width is None:
            self.width = screen.get_width() * 3 // 4
        else:
            self.width = width
        self.color = color
        self.progress_color = progress_color
        self.textColor = textColor
        self.progress = 0
        self.text = ""
    
    def setProgress(self, progress):
        self.progress = progress
    
    def setText(self, text):
        self.text = text
    
    def draw(self, x=None, y=None):
        if x is None:
            x = (self.screen.get_width() - self.width) // 2
        if y is None:
            y = self.screen.get_height() - self.height - 10
        
        # Draw the background bar
        pygame.draw.rect(self.screen, self.color, (x, y, self.width, self.height))
        
        # Draw the progress bar
        progress_width = int(self.width * self.progress)
        if self.progress > 1: progress_width = self.width
        pygame.draw.rect(self.screen, self.progress_color, (x, y, progress_width, self.height))
        
        # Draw the text
        text_surface = self.font.render(self.text, True, self.textColor)
        text_x = x + (self.width - text_surface.get_width()) // 2
        text_y = y + (self.height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))