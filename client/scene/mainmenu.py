import pygame

class MainMenu():
	def __init__(self, screen, dataManager):
		self.screen = screen
		self.dataManager = dataManager

	def render(self):
		self.screen.fill((255, 255, 255))
		pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
		