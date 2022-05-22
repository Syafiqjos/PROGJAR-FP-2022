import sys
sys.path.append('..')

from Library.Sprite import Sprite

import pygame

class GameplayScene():
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.eventManager = self.gameManager.eventManager
		self.screen = self.gameManager.screen
		self.sprites = { 'ALL': [], 'PLANTS': [], 'ZOMBIES': [], 'PAUSED': [] }
		self.objects = {}
		self.isPaused = False

		self.awake()

	def awake(self):
		self.state = 'PLANTS' # 'ALL', 'ZOMBIES', 'PAUSED'

		self.awakeAll()
		self.awakePaused()
		if self.state == 'PLANTS':
			self.awakePlants()
		elif self.state == 'ZOMBIES':
			self.awakeZombies()
		
	def awakeAll(self):
		# Background
		tilePivot = (60, 140)
		for i in range(0, 10): # x
			for j in range(0, 5): # y
				objName = 'all_bgTile' + str(i) + 'x' + str(j)
				tileSize = 60
				tileScale = 3
				posX = tilePivot[0] + i * tileSize
				posY = tilePivot[1] + j * tileSize
				self.objects[objName] = Sprite(self.screen, (posX, posY), (tileScale, tileScale), 'Assets/kenney_pixelshmup/Tiles/tile_0110.png')
				self.sprites['ALL'].append(self.objects[objName])

		# Matahari UI
		# Drag Drop UI
		# Seluruh plants
		# Seluruh zombies

	def awakePaused(self):
		# Foreground paused UI
		pass

	def awakePlants(self):
		# Matahari Plants
		pass

	def awakeZombies(self):
		# Matahari Zombies
		pass

	def eventsAll(self, event):
		pass

	def eventsPlants(self, event):
		pass

	def eventsZombies(self, event):
		pass

	def eventsPaused(self, event):
		pass

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gameManager.running = False
			if self.isPaused:
				self.eventsPaused(event)
			else:
				self.eventsAll(event)
				if self.state == 'PLANTS':
					self.eventsPlants(event)
				if self.state == 'ZOMBIES':
					self.eventsZombies(event)

	def render(self):
		self.screen.fill((0, 0, 0))
		
		for sprite in self.sprites['ALL']:
			sprite.render()
		for sprite in self.sprites[self.state]:
			sprite.render()

	def pauseGame(self):
		self.isPaused = True

	def disconnectToMainMenu(self):
		self.gameManager.loadScene('MainMenu')

	def unpauseGame(self):
		self.isPaused = False