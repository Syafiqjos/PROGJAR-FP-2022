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
		self.drawTileBatch('all_bgTile', 'ALL', (30 + 60, 140), (9, 5), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0110.png')

		# Plant Greaser Tile
		self.drawTileBatch('all_bgPlantGreaserTile', 'ALL', (30 + 0, 140), (1, 5), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0076.png')

		# Zombie Deploy Tile
		self.drawTileBatch('all_bgZombieDeployTile', 'ALL', (30 + 60 * 10, 140), (1, 5), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0077.png')

		# Matahari UI
		self.drawTileBatch('all_matahariUI', 'ALL', (10, 10), (1, 1), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0054.png')

		# Drag Drop UI
		self.drawTileBatch('all_matahariUITile', 'ALL', (10 + 60, 10), (6, 1), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0044.png')
		
		# Pause Button
		self.drawSprite('all_pauseButton', 'ALL', (650, 10), (1, 1), 'Assets/gameicons/PNG/White/1x/pause.png')

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

	def drawTileBatch(self, objectNamespace, state, pivot, length, tileSize, tileScale, imagePath):
		tilePivot = pivot
		for i in range(0, length[0]): # x
			for j in range(0, length[1]): # y
				objName = objectNamespace + str(i) + 'x' + str(j)
				posX = tilePivot[0] + i * tileSize
				posY = tilePivot[1] + j * tileSize
				self.drawSprite(objName, state, (posX, posY), (tileScale, tileScale), imagePath)

	def drawSprite(self, objName, state, pos, scale, imagePath):
		self.objects[objName] = Sprite(self.screen, (pos[0], pos[1]), (scale[0], scale[1]), imagePath)
		self.sprites[state].append(self.objects[objName])

	def eventsAll(self, event):
		# pause button
		if self.eventManager.checkOnClick(event, self.objects['all_pauseButton']):
			self.pauseGame()

		# bg tile
		for i in range(0, 9): # x
			for j in range(0, 5): # y
				objectName = 'all_bgTile' + str(i) + 'x' + str(j)
				if objectName in self.objects:
					if self.eventManager.checkOnClick(event, self.objects[objectName]):
						self.sprites['ALL'].remove(self.objects[objectName])
						del self.objects[objectName]
						print('BG TILE :' + objectName)

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