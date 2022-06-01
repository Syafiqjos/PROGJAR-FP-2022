import string
import pygame

class Display():

    def __init__(self, text, screen, position, size=32, color='white'):
        self.isRender = True

        self.screen = screen #game load screen
        self.color = color # (R,G,B)
        self.size = size
        self.font = pygame.font.Font('Assets/Font/Sunflower.otf', self.size)
        self.text = text
        self.position = position
        self.texting()


    def texting(self):
        self.text = self.font.render(self.text, True, self.color)
        self.textRect = self.text.get_rect()
        self.textRect.center = self.position
    

    def awake(self):
        self.screen.blit(self.text,self.textRect)

    def update(self):
        pass