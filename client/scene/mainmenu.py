import pygame

class MainMenu():
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.screen = self.gameManager.screen

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gameManager.running = False

	def render(self):
		self.screen.fill((255, 255, 255))
		pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
		