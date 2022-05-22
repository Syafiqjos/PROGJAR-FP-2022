import sys
sys.path.append('..')

from Library.Sprite import Sprite

import pygame

class LobbyMenu():
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.eventManager = self.gameManager.eventManager
		self.screen = self.gameManager.screen
		self.sprites = []

		self.awake()

	def awake(self):
		self.state = 'HOME' # 'CREATE', 'JOIN'

		self.backMainMenuButton = Sprite(self.screen, (100, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/home.png')
		self.createRoomButton = Sprite(self.screen, (300, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/import.png')
		self.joinRoomButton = Sprite(self.screen, (500, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/exitRight.png')

		self.sprites.append(self.createRoomButton)
		self.sprites.append(self.joinRoomButton)
		self.sprites.append(self.backMainMenuButton)
		

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gameManager.running = False
			if self.state == 'HOME':
				if self.eventManager.checkOnClick(event, self.createRoomButton):
					print('create room')
					self.goToCreateRoom()
				elif self.eventManager.checkOnClick(event, self.joinRoomButton):
					print('join room')
					self.goToJoinRoom()
				elif self.eventManager.checkOnClick(event, self.backMainMenuButton):
					print('go main menu')
					self.goToMainMenu()

	def render(self):
		self.screen.fill((0, 0, 0))
		
		for sprite in self.sprites:
			sprite.render()

	def goToCreateRoom(self):
		self.state = 'CREATE'

	def goToJoinRoom(self):
		self.state = 'JOIN'

	def goToHome(self):
		self.state = 'HOME'

	def goToMainMenu(self):
		self.gameManager.loadScene('MainMenu')