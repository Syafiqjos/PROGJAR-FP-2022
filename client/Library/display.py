import pygame

class display():
    def __init__(self, text, screen, position):
        self.isRender = True

        self.screen = screen #game load screen
        self.color = (254, 254, 254) # (R,G,B)
        self.size = 32
        self.font = pygame.font.Font('Assets/Font/Sunflower.otf', self.size) 
        self.texting(screen, text, position)


    def texting(self, txt, position):
        self.text = self.font.render(txt, True, self.color, (255,255,255))
        self.textRect = self.text.get_rect()
        self.textRect.center = position
        self.screen.blit(self.text,self.textRect)

    def setSize(self, size):
        self.size = size

    def setColor(self, color):
        self.color = color
    

    def awake(self):
        pass

    def update(self):
        pass
