import sys
sys.path.append('..')

from Library.Sprite import Sprite

import pygame

class MainMenu():
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.screen = self.gameManager.screen
		self.sprites = []

		self.awake()

	def awake(self):
		self.robot = Sprite(self.screen, (0, 0), (0.2, 0.2), 'Assets/robotball/skeleton-animation_01.png')

		self.sprites.append(self.robot)
		

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gameManager.running = False

	def render(self):
		self.screen.fill((255, 255, 255))
		pygame.draw.circle(self.screen, (0, 0, 255), (250, 250), 75)
		
		for sprite in self.sprites:
			sprite.render()
		