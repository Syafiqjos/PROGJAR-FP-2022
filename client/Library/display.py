import pygame

class Display():
    def __init__(self, text, screen, position, size, color):
        self.isRender = True

        self.screen = screen #game load screen
        self.color = color # (R,G,B)
        self.size = size
        self.font = pygame.font.Font('Assets/Font/Sunflower.otf', self.size) 
        self.texting(screen, text, position)


    def texting(self, screen, txt, position):
        self.text = self.font.render(txt, True, self.color)
        self.textRect = self.text.get_rect()
        self.textRect.center = position
        self.screen.blit(self.text,self.textRect)
    

    def awake(self):
        pass

    def update(self):
        pass
