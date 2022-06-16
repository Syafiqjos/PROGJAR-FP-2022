import sys
sys.path.append('..')

from Library.Sprite import Sprite
from Library.Display import Display

import pygame

class LobbyMenu():
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.eventManager = self.gameManager.eventManager
		self.screen = self.gameManager.screen
		self.sprites = { 'HOME': [], 'CREATE': [], 'JOIN': [] }
		self.objects = {}

		self.awake()

		self.waiting = 120
		self.waited = False

	def awake(self):
		self.state = 'HOME' # 'CREATE', 'JOIN'

		self.awakeHome()
		self.awakeCreate()
		self.awakeJoin()
		
	def awakeHome(self):
		self.objects['home_backMainMenuButton'] = Sprite(self.screen, (100, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/home.png')
		self.objects['home_createRoomButton'] = Sprite(self.screen, (300, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/import.png')
		self.objects['home_joinRoomButton'] = Sprite(self.screen, (500, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/exitRight.png')

		state = 'HOME'
		# self.sprites[state].append(self.objects['home_backMainMenuButton'])
		# self.sprites[state].append(self.objects['home_createRoomButton'])
		# self.sprites[state].append(self.objects['home_joinRoomButton'])

		self.objects['home_otherPlayerDisconnectedText'] = Display('Other Player Disconnected', self.screen, (240, 100), 24, (255, 255, 255));
		self.objects['home_returningToMainMenuText'] = Display('Returning to Main Menu..', self.screen, (240, 300), 18, (255, 255, 255));

		self.sprites[state].append(self.objects['home_otherPlayerDisconnectedText'])
		self.sprites[state].append(self.objects['home_returningToMainMenuText'])

	def awakeCreate(self):
		self.objects['create_backHomeButton'] = Sprite(self.screen, (100, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/home.png')

		state = 'CREATE'
		self.sprites[state].append(self.objects['create_backHomeButton'])

	def awakeJoin(self):
		self.objects['join_backHomeButton'] = Sprite(self.screen, (100, 100), (1, 1), 'Assets/gameicons/PNG/White/1x/home.png')

		state = 'JOIN'
		self.sprites[state].append(self.objects['join_backHomeButton'])

	def eventsHome(self, event):
		if self.eventManager.checkOnClick(event, self.objects['home_createRoomButton']):
			print('create room')
			self.goToCreateRoom()
		elif self.eventManager.checkOnClick(event, self.objects['home_joinRoomButton']):
			print('join room')
			self.goToJoinRoom()
		elif self.eventManager.checkOnClick(event, self.objects['home_backMainMenuButton']):
			print('go main menu')
			self.goToMainMenu()

	def eventsCreate(self, event):
		if self.eventManager.checkOnClick(event, self.objects['create_backHomeButton']):
			print('home room')
			self.goToHome()

	def eventsJoin(self, event):
		if self.eventManager.checkOnClick(event, self.objects['join_backHomeButton']):
			print('home room')
			self.goToHome()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gameManager.running = False
			if self.state == 'HOME':
				self.eventsHome(event)
			elif self.state == 'CREATE':
				self.eventsCreate(event)
			elif self.state == 'JOIN':
				self.eventsJoin(event)

	def render(self):
		self.screen.fill((0, 0, 0))
		
		for sprite in self.sprites[self.state]:
			sprite.render()

		self.update()

	def update(self):
		if self.waited == False:
			if self.waiting > 0:
				self.waiting = self.waiting - 1
			else:
				self.waited = True
				print('Go to Main Menu')
				self.gameManager.loadScene('MainMenu')

	def goToCreateRoom(self):
		self.state = 'CREATE'

	def goToJoinRoom(self):
		self.state = 'JOIN'

	def goToHome(self):
		self.state = 'HOME'

	def goToMainMenu(self):
		self.gameManager.loadScene('MainMenu')