import sys
sys.path.append('..')

from Library.Sprite import Sprite

import pygame
import random

class MatahariOrb(Sprite):
	def awake(self):
		self.stopFallPos = 80 + random.random() * 320

	def update(self):
		if self.position[1] < self.stopFallPos:
			self.setPosition((self.position[0], self.position[1] + 1))

class GameplayScene():
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.eventManager = self.gameManager.eventManager
		self.screen = self.gameManager.screen
		self.sprites = { 'ALL': [], 'PLANTS': [], 'ZOMBIES': [], 'PAUSED': [], 'UI': [] }
		self.objects = {}
		self.isPaused = False

		self.plantsOrbs = []
		self.plantsMatahariTimerMax = 200
		self.plantsMatahariTimer = self.plantsMatahariTimerMax

		self.awake()

	def awake(self):
		self.state = 'PLANTS' # 'ALL', 'ZOMBIES', 'UI', 'PAUSED'

		self.awakeAll()
		if self.state == 'PLANTS':
			self.awakePlants()
		elif self.state == 'ZOMBIES':
			self.awakeZombies()
		self.awakeUI()
		self.awakePaused()
		
	def awakeAll(self):
		# Background
		self.drawTileBatch('all_bgTile', 'ALL', (30 + 60, 140), (9, 5), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0110.png')

		# Plant Greaser Tile
		self.drawTileBatch('all_bgPlantGreaserTile', 'ALL', (30 + 0, 140), (1, 5), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0076.png')

		# Zombie Deploy Tile
		self.drawTileBatch('all_bgZombieDeployTile', 'ALL', (30 + 60 * 10, 140), (1, 5), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0077.png')

		# Seluruh plants
		# Seluruh zombies

	def awakeUI(self):
		# Matahari UI
		self.drawTileBatch('ui_matahariUI', 'UI', (10, 10), (1, 1), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0054.png')

		# Drag Drop UI
		self.drawTileBatch('ui_matahariUITile', 'UI', (10 + 60, 10), (6, 1), 60, 3, 'Assets/kenney_pixelshmup/Tiles/tile_0044.png')
		
		# Pause Button
		self.drawSprite('ui_pauseButton', 'UI', (650, 10), (1, 1), 'Assets/gameicons/PNG/White/1x/pause.png')

	def awakePaused(self):
		# Foreground paused UI
		self.drawSprite('paused_bgPause', 'PAUSED', (80, 80), (36, 20), 'Assets/kenney_pixelshmup/Tiles/tile_0115.png')
		self.drawSprite('paused_unpauseButton', 'PAUSED', (240, 240), (1, 1), 'Assets/gameicons/PNG/White/1x/forward.png')
		self.drawSprite('paused_disconnectButton', 'PAUSED', (120, 240), (1, 1), 'Assets/gameicons/PNG/White/1x/door.png')

	def awakePlants(self):
		self.plantsSpawnRandomMatahari()

	def awakeZombies(self):
		# Matahari Zombies
		pass

	def plantsSpawnRandomMatahari(self):
		posX = 20 + random.random() * (320 - 20)
		self.plantsOrbs.append(MatahariOrb(self.screen, (posX, 0), (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0000.png'))

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
		# bg tile
		for i in range(0, 9): # x
			for j in range(0, 5): # y
				objectName = 'all_bgTile' + str(i) + 'x' + str(j)
				if objectName in self.objects:
					if self.eventManager.checkOnClick(event, self.objects[objectName]):
						self.sprites['ALL'].remove(self.objects[objectName])
						del self.objects[objectName]
						print('BG TILE :' + objectName)

	def eventsUI(self, event):
		# pause button
		if self.eventManager.checkOnClick(event, self.objects['ui_pauseButton']):
			self.pauseGame()

	def eventsPlants(self, event):
		for orb in self.plantsOrbs:
			if self.eventManager.checkOnClick(event, orb):
				self.plantsOrbs.remove(orb)
				print('PLANTS ORB OBTAINED')

	def eventsZombies(self, event):
		pass

	def eventsPaused(self, event):
		# unpause button
		if self.eventManager.checkOnClick(event, self.objects['paused_unpauseButton']):
			self.unpauseGame()
		# disconnect
		if self.eventManager.checkOnClick(event, self.objects['paused_disconnectButton']):
			self.disconnectToMainMenu()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gameManager.running = False
			if self.isPaused:
				self.eventsPaused(event)
			else:
				self.eventsAll(event)
				self.eventsUI(event)
				if self.state == 'PLANTS':
					self.eventsPlants(event)
				if self.state == 'ZOMBIES':
					self.eventsZombies(event)

	def render(self):
		self.update()
		self.screen.fill((0, 0, 0))
		
		for sprite in self.sprites['ALL']:
			sprite.render()
		for sprite in self.sprites[self.state]:
			sprite.render()
		if self.state == 'PLANTS':
			for sprite in self.plantsOrbs:
				sprite.render()
		for sprite in self.sprites['UI']:
			sprite.render()
		if self.isPaused:
			for sprite in self.sprites['PAUSED']:
				sprite.render()

	def update(self):
		if self.state == 'PLANTS':
			self.updatePlants()

	def updatePlants(self):
		if self.plantsMatahariTimer > 0:
			self.plantsMatahariTimer -= 1
		else:
			self.plantsMatahariTimer = self.plantsMatahariTimerMax
			self.plantsSpawnRandomMatahari()

	def pauseGame(self):
		self.isPaused = True

	def disconnectToMainMenu(self):
		self.gameManager.loadScene('MainMenu')

	def unpauseGame(self):
		self.isPaused = False