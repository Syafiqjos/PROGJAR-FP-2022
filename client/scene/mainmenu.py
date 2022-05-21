import pygame

class mainmenu():
	def __init__(self, screen):
		self.screen = screen

	def render(self):
		self.screen.fill((255, 255, 255))
		pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
		