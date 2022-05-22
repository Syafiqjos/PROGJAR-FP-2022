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
		self.drawTileBatch((30 + 60, 140), (10, 5), 'all_bgTile', 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0110.png')

		# Plant Greaser Tile
		self.drawTileBatch((30 + 0, 140), (1, 5), 'all_bgPlantGreaserTile', 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0076.png')

		# Zombie Deploy Tile
		self.drawTileBatch((30 + 60 * 10, 140), (1, 5), 'all_bgZombieDeployTile', 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0077.png')

		# Matahari UI
		self.drawTileBatch((10, 10), (1, 1), 'all_matahariUI', 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0054.png')

		# Drag Drop UI
		self.drawTileBatch((10 + 60, 10), (6, 1), 'all_matahariUITile', 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0044.png')

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

	def drawTileBatch(self, pivot, length, objectNamespace, tileSize, tileScale, imagePath):
		tilePivot = pivot
		for i in range(0, length[0]): # x
			for j in range(0, length[1]): # y
				objName = objectNamespace + str(i) + 'x' + str(j)
				posX = tilePivot[0] + i * tileSize
				posY = tilePivot[1] + j * tileSize
				self.objects[objName] = Sprite(self.screen, (posX, posY), (tileScale, tileScale), imagePath)
				self.sprites['ALL'].append(self.objects[objName])

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