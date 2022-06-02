import sys
sys.path.append('..')

import pygame
import random

from Library.Sprite import Sprite
from Library.GameEntities import MatahariOrb
from Library.GameEntities import PeluruBuncis
from Library.GameEntities import Tumbuhan
from Library.GameEntities import TumbuhanKentang
from Library.GameEntities import TumbuhanBuncisNormal
from Library.GameEntities import TumbuhanBuncisJago
from Library.GameEntities import MatahariOrb
from Library.GameEntities import ZombieWalker
from Library.GameEntities import ZombieWalkerNormal
from Library.GameEntities import ZombieWalkerJago
from Library.GameEntities import ZombieWalkerHandal
from Library.GameMessageReceiver import GameMessageReceiver

class GameplayScene():
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.eventManager = self.gameManager.eventManager
		self.socketManager = self.gameManager.socketManager
		self.accountSocket = self.gameManager.accountSocket
		self.gameSocket = self.gameManager.gameSocket

		self.gameMessageReceiver = GameMessageReceiver(self.socketManager.connection)
		self.gameMessageReceiver.subscribeEventListener(self.eventTrigger)
		self.gameMessageReceiver.start()

		self.screen = self.gameManager.screen
		self.sprites = { 'ALL': [], 'ALLPLANTS': [], 'ALLZOMBIES': [], 'PLANTS': [], 'ZOMBIES': [], 'PAUSED': [], 'UI': [] }
		self.objects = {}
		self.isPaused = False

		# waktu
		self.clock = pygame.time.Clock()

		self.plantsGameTimer = 60 * 60 * (1) # 1 minutes
		self.plantsOrbs = []
		self.plantsMatahariTimerMax = 200
		self.plantsMatahariTimer = self.plantsMatahariTimerMax

		self.plantsBullets = []

		self.zombiesOrbs = []
		self.zombiesIndex = 0
		self.zombiesMatahariTimerMax = 200
		self.zombiesMatahariTimer = self.zombiesMatahariTimerMax

		self.selectedDD = None

		self.awake()

	def awake(self):
		self.state = 'ZOMBIES' # 'ALL', 'ZOMBIES', 'UI', 'PAUSED'

		if self.dataManager.get('user_role') == 'zombie':
			self.state = 'ZOMBIES'
		elif self.dataManager.get('user_role') == 'plant':
			self.state = 'PLANTS'

		self.resetCurrency()

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
		if self.state == 'PLANTS':
			plantsDDPivot = (8, 6)
			self.drawSprite('ui_plantsDD1', 'UI', (plantsDDPivot[0] + 10 + 60 + 60 * 0, plantsDDPivot[1] + 10), (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0001.png')
			self.drawSprite('ui_plantsDD2', 'UI', (plantsDDPivot[0] + 10 + 60 + 60 * 1, plantsDDPivot[1] + 10), (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0002.png')
			self.drawSprite('ui_plantsDD3', 'UI', (plantsDDPivot[0] + 10 + 60 + 60 * 2, plantsDDPivot[1] + 10), (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0003.png')
			self.drawSprite('ui_plantsDD4', 'UI', (plantsDDPivot[0] + 10 + 60 + 60 * 3, plantsDDPivot[1] + 10), (1, 1), 'Assets/kenney_pixelshmup/Ships/ship_0004.png')
		elif self.state == 'ZOMBIES':
			plantsDDPivot = (8, 6)
			self.drawSprite('ui_zombiesDD1', 'UI', (plantsDDPivot[0] + 10 + 60 + 60 * 0, plantsDDPivot[1] + 10), (0.08, 0.08), 'Assets/robotball/skeleton-animation_01.png')
			self.drawSprite('ui_zombiesDD2', 'UI', (plantsDDPivot[0] + 10 + 60 + 60 * 1, plantsDDPivot[1] + 10), (0.08, 0.08), 'Assets/robotball/skeleton-animation_03.png')
			self.drawSprite('ui_zombiesDD3', 'UI', (plantsDDPivot[0] + 10 + 60 + 60 * 2, plantsDDPivot[1] + 10), (0.08, 0.08), 'Assets/robotball/skeleton-animation_05.png')

		self.drawSprite('ui_DDSelect', 'UI', (650, 10), (1, 1), 'Assets/gameicons/PNG/White/1x/tablet.png')
		self.objects['ui_DDSelect'].isRender = False
		
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
		self.zombiesSpawnRandomMatahari()
		self.plantsPlaceDD('ui_plantsDD1', 'all_bgTile0x0', self.objects['all_bgTile0x0'])
		self.plantsPlaceDD('ui_plantsDD2', 'all_bgTile1x1', self.objects['all_bgTile1x1'])
		self.plantsPlaceDD('ui_plantsDD3', 'all_bgTile1x2', self.objects['all_bgTile1x2'])

	def plantsSpawnRandomMatahari(self):
		posX = 20 + random.random() * (320 - 20)
		self.plantsSpawnMatahari((posX, 0))

	def plantsSpawnMatahari(self, position):
		sprite = MatahariOrb(self.screen, position)
		sprite.setup(self)
		self.plantsOrbs.append(sprite)
		return sprite

	def zombiesSpawnRandomMatahari(self):
		posX = 360 + random.random() * (320 - 20)
		self.zombiesSpawnMatahari((posX, 0))

	def zombiesSpawnMatahari(self, position):
		sprite = MatahariOrb(self.screen, position)
		sprite.setup(self)
		self.zombiesOrbs.append(sprite)
		return sprite

	def resetCurrency(self):
		self.dataManager.set('gameplay_currency', 0)

	def pickMatahari(self):
		matahariCurrency = 25
		currentCurrency = self.dataManager.get('gameplay_currency')
		self.setCurrency(currentCurrency + 25)

	def setCurrency(self, currency):
		self.dataManager.set('gameplay_currency', currency)

	def getCurrency(self):
		return self.dataManager.get('gameplay_currency')

	def drawTileBatch(self, objectNamespace, state, pivot, length, tileSize, tileScale, imagePath):
		tilePivot = pivot
		for i in range(0, length[0]): # x
			for j in range(0, length[1]): # y
				objName = objectNamespace + str(i) + 'x' + str(j)
				posX = tilePivot[0] + i * tileSize
				posY = tilePivot[1] + j * tileSize
				self.drawSprite(objName, state, (posX, posY), (tileScale, tileScale), imagePath)

	def drawSprite(self, objName, state, pos, scale, imagePath):
		self.registerSprite(objName, state, Sprite(self.screen, (pos[0], pos[1]), (scale[0], scale[1]), imagePath))

	def registerSprite(self, objName, state, sprite):
		self.objects[objName] = sprite
		self.sprites[state].append(sprite)

	def eventsAll(self, event):
		bgTilePressed = False
		bgTilePressedName = None
		bgTilePressedObj = None

		# bg tile
		for i in range(0, 9): # x
			for j in range(0, 5): # y
				objectName = 'all_bgTile' + str(i) + 'x' + str(j)
				if objectName in self.objects:
					if self.eventManager.checkOnClick(event, self.objects[objectName]):
						# self.sprites['ALL'].remove(self.objects[objectName])
						# del self.objects[objectName]
						bgTilePressed = True
						bgTilePressedName = objectName
						bgTilePressedObj = self.objects[objectName]
						print('BG TILE :' + objectName)

		if bgTilePressed and self.selectedDD != None:
			print('Place DD of: ' + self.selectedDD + ' into ' + bgTilePressedName)
			messagePlacing = self.placeSelectedDD(bgTilePressedName, bgTilePressedObj)
			if messagePlacing == 'NOMONEY':
				print('No Money')
			elif messagePlacing == 'OCCUPIED':
				print('Tile was occupied')
			self.unselectDD()
		elif self.selectedDD != None and self.eventManager.checkOnClickAny(event):
			self.unselectDD()

	def eventsUI(self, event):
		# pause button
		if self.eventManager.checkOnClick(event, self.objects['ui_pauseButton']):
			self.pauseGame()

	def eventsPlants(self, event):
		for orb in self.plantsOrbs:
			if self.eventManager.checkOnClick(event, orb):
				self.plantsOrbs.remove(orb)
				self.pickMatahari()
				print('PLANTS ORB OBTAINED, CURRENCY: ' + str(self.getCurrency()))

		if self.eventManager.checkOnClick(event, self.objects['ui_plantsDD1']):
			self.selectDD(self.objects['ui_plantsDD1'], 'ui_plantsDD1')
		elif self.eventManager.checkOnClick(event, self.objects['ui_plantsDD2']):
			self.selectDD(self.objects['ui_plantsDD2'], 'ui_plantsDD2')
		elif self.eventManager.checkOnClick(event, self.objects['ui_plantsDD3']):
			self.selectDD(self.objects['ui_plantsDD3'], 'ui_plantsDD3')
		elif self.eventManager.checkOnClick(event, self.objects['ui_plantsDD4']):
			self.selectDD(self.objects['ui_plantsDD4'], 'ui_plantsDD4')

	def eventsZombies(self, event):
		for orb in self.zombiesOrbs:
			if self.eventManager.checkOnClick(event, orb):
				self.zombiesOrbs.remove(orb)
				self.pickMatahari()
				print('ZOMBIES ORB OBTAINED, CURRENCY: ' + str(self.getCurrency()))

		if self.eventManager.checkOnClick(event, self.objects['ui_zombiesDD1']):
			self.selectDD(self.objects['ui_zombiesDD1'], 'ui_zombiesDD1')
		elif self.eventManager.checkOnClick(event, self.objects['ui_zombiesDD2']):
			self.selectDD(self.objects['ui_zombiesDD2'], 'ui_zombiesDD2')
		elif self.eventManager.checkOnClick(event, self.objects['ui_zombiesDD3']):
			self.selectDD(self.objects['ui_zombiesDD3'], 'ui_zombiesDD3')

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
				self.gameMessageReceiver.close()
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
		for sprite in self.sprites['ALLPLANTS']:
			sprite.render()
		for sprite in self.sprites['ALLZOMBIES']:
			sprite.render()
		for sprite in self.sprites[self.state]:
			sprite.render()
		for sprite in self.plantsBullets:
			sprite.render()
		if self.state == 'PLANTS':
			for sprite in self.plantsOrbs:
				sprite.render()
		if self.state == 'ZOMBIES':
			for sprite in self.zombiesOrbs:
				sprite.render()
		for sprite in self.sprites['UI']:
			sprite.render()
		if self.isPaused:
			for sprite in self.sprites['PAUSED']:
				sprite.render()

	def update(self):
		if self.state == 'PLANTS':
			self.updatePlants()
		elif self.state == 'ZOMBIES':
			self.updateZombies()

	def updatePlants(self):
		if self.plantsMatahariTimer > 0:
			self.plantsMatahariTimer -= 1
		else:
			self.plantsMatahariTimer = self.plantsMatahariTimerMax
			self.plantsSpawnRandomMatahari()

		# game timer, when time up then the plants win
		if self.plantsGameTimer > 0:
			self.plantsGameTimer -= 1
			if int(self.plantsGameTimer) % (60 * 5) == 0:
				print(int(self.plantsGameTimer / 60), 'seconds left to win the game.')
		else:
			self.triggerPlantsWin()

	def updateZombies(self):
		if self.zombiesMatahariTimer > 0:
			self.zombiesMatahariTimer -= 1
		else:
			self.zombiesMatahariTimer = self.zombiesMatahariTimerMax
			self.zombiesSpawnRandomMatahari()

	def pauseGame(self):
		self.isPaused = True

	def disconnectToMainMenu(self):
		self.gameManager.loadScene('MainMenu')

	def unpauseGame(self):
		self.isPaused = False

	def selectDD(self, toBeSelected, name):
		selectObj = self.objects['ui_DDSelect']
		selectObj.isRender = True
		selectObj.setPosition(toBeSelected.position)
		self.selectedDD = name

	def unselectDD(self):
		selectObj = self.objects['ui_DDSelect']
		selectObj.isRender = False
		self.selectedDD = None

	def placeSelectedDD(self, tileName, tileObj):
		if self.state == 'PLANTS':
			return self.plantsPlaceSelectedDD(tileName, tileObj)
		elif self.state == 'ZOMBIES':
			return self.zombiesPlaceSelectedDD(tileName, tileObj)
		return None

	def plantsPlaceSelectedDD(self, tileName, tileObj):
		price = self.getPriceDD(self.selectedDD)
		occupiedName = 'allplants_plantsDD:' + tileName
		# if price not 0 (not gonna clear this tile) and tile is occupied
		if price != 0 and occupiedName in self.objects:
			return 'OCCUPIED'
		elif price > self.getCurrency():
			return 'NOMONEY'
		self.setCurrency(self.getCurrency() - price)
		self.placeDD(self.selectedDD, tileName, tileObj)
		print('DD Placed.')
		return None

	def zombiesPlaceSelectedDD(self, tileName, tileObj):
		price = self.getPriceDD(self.selectedDD)
		if price > self.getCurrency():
			return 'NOMONEY'
		self.setCurrency(self.getCurrency() - price)
		self.placeDD(self.selectedDD, tileName, tileObj)
		print('DD Placed.')
		return None

	def getPriceDD(self, ddName):
		if self.state == 'PLANTS':
			return self.plantsGetPriceDD(ddName)
		elif self.state == 'ZOMBIES':
			return self.zombiesGetPriceDD(ddName)

		return 1000000

	def plantsGetPriceDD(self, ddName):
		if ddName == 'ui_plantsDD1':
			return 25
		elif ddName == 'ui_plantsDD2':
			return 100
		elif ddName == 'ui_plantsDD3':
			return 200
		elif ddName == 'ui_plantsDD4':
			return 0

		return 1000000

	def zombiesGetPriceDD(self, ddName):
		if ddName == 'ui_zombiesDD1':
			return 50
		elif ddName == 'ui_zombiesDD2':
			return 100
		elif ddName == 'ui_zombiesDD3':
			return 200

		return 1000000

	def placeDD(self, ddName, tileName, tileObj):
		if self.state == 'PLANTS':
			self.plantsPlaceDD(ddName, tileName, tileObj)
		elif self.state == 'ZOMBIES':
			self.zombiesPlaceDD(ddName, tileName, tileObj)

	def plantsPlaceDD(self, ddName, tileName, tileObj):
		spriteName = 'allplants_plantsDD:' + tileName
		if ddName == 'ui_plantsDD1':
			sprite = TumbuhanKentang(self.screen, tileObj.position)
			sprite.setup(spriteName, self)
			self.registerSprite(spriteName, 'ALLPLANTS', sprite)
			self.triggerPlantSpawn(tileName, sprite)
		elif ddName == 'ui_plantsDD2':
			sprite = TumbuhanBuncisNormal(self.screen, tileObj.position)
			sprite.setup(spriteName, self)
			self.registerSprite(spriteName, 'ALLPLANTS', sprite)
			self.triggerPlantSpawn(tileName, sprite)
		elif ddName == 'ui_plantsDD3':
			sprite = TumbuhanBuncisJago(self.screen, tileObj.position)
			sprite.setup(spriteName, self)
			self.registerSprite(spriteName, 'ALLPLANTS', sprite)
			self.triggerPlantSpawn(tileName, sprite)
		elif ddName == 'ui_plantsDD4':
			if spriteName in self.objects:
				self.triggerPlantDie(self.objects[spriteName])
				self.sprites['ALLPLANTS'].remove(self.objects[spriteName])
				del self.objects[spriteName]

	def zombiesPlaceDD(self, ddName, tileName, tileObj):
		spriteName = 'allzombies_zombiesDD:' + str(self.zombiesIndex)
		self.zombiesIndex += 1
		if ddName == 'ui_zombiesDD1':
			sprite = ZombieWalkerNormal(self.screen, tileObj.position)
			sprite.setup(spriteName, self)
			self.registerSprite(spriteName, 'ALLZOMBIES', sprite)
			self.triggerZombieSpawn(tileName, sprite)
		elif ddName == 'ui_zombiesDD2':
			sprite = ZombieWalkerJago(self.screen, tileObj.position)
			sprite.setup(spriteName, self)
			self.registerSprite(spriteName, 'ALLZOMBIES', sprite)
			self.triggerZombieSpawn(tileName, sprite)
		elif ddName == 'ui_zombiesDD3':
			sprite = ZombieWalkerHandal(self.screen, tileObj.position)
			sprite.setup(spriteName, self)
			self.registerSprite(spriteName, 'ALLZOMBIES', sprite)
			self.triggerZombieSpawn(tileName, sprite)

	def triggerPlantsWin(self):
		if self.state == 'PLANTS':
			print('PLANTS WINS!!')
			res = self.gameSocket.sendWinnerEvent('plant')
			print(res)
			self.gameManager.loadScene('MainMenu')

	def triggerZombiesWin(self):
		if self.state == 'ZOMBIES':
			print('ZOMBIES WINS!!')
			res = self.gameSocket.sendWinnerEvent('zombie')
			print(res)
			self.gameManager.loadScene('MainMenu')

	def triggerPlantDie(self, plant):
		if self.state == 'PLANTS':
			print('A PLANT DIE!!')
			res = self.gameSocket.sendPlantDieEvent(plant)
			print(res)

	def triggerZombieDie(self, zombie):
		if self.state == 'ZOMBIES':
			print('A ZOMBIE DIE!!')
			res = self.gameSocket.sendZombieDieEvent(zombie)
			print(res)

	def triggerPlantSpawn(self, tile, plant):
		if self.state == 'PLANTS':
			print('A PLANT SPAWNED!!')
			res = self.gameSocket.sendPlantSpawnEvent(tile, plant)
			print(res)

	def triggerZombieSpawn(self, tile, zombie):
		if self.state == 'ZOMBIES':
			print('A ZOMBIE SPAWNED!!')
			res = self.gameSocket.sendZombieSpawnEvent(tile, zombie)
			print(res)

	def triggerPlantShoot(self, plant):
		if self.state == 'PLANTS':
			print('A PLANT SHOOTED!!')
			res = self.gameSocket.sendPlantShootEvent(plant)
			print(res)

	def eventTrigger(self, data):
		print('message received from event trigger')
		print(data)

		event = data['event']

		if event == 'on_winner':
			self.receiveTriggerWinner(data)

	def receiveTriggerWinner(self, data):
		if data['winner'] == 'plant':
			self.dataManager.set('user_winner', 'plant')
			self.gameManager.loadScene('MainMenu')
		elif data['winner'] == 'zombie':
			self.dataManager.set('user_winner', 'zombie')
			self.gameManager.loadScene('MainMenu')