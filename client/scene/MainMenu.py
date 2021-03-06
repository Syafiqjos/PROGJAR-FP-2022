import sys

sys.path.append("..")

from Library.Sprite import Sprite
from Library.Display import Display

import pygame


class MainMenu:
	def __init__(self, gameManager):
		self.gameManager = gameManager
		self.dataManager = self.gameManager.dataManager
		self.eventManager = self.gameManager.eventManager
		self.screen = self.gameManager.screen
        
		self.spritesMenu = []
		self.spritesLoading = []
		self.bg = pygame.image.load('Assets/our/potato-wallpaper.jpg')
		self.bg = pygame.transform.scale(self.bg,(720,480))

		self.state = 'MENU' # MENU | LOADING

		self.will_find_match = False
		self.find_match_timer = 60

		self.awake()

	def awake(self):
		self.playAsPlantsButton = Sprite(
			self.screen, (260, 100 - 20), (1, 1), "Assets/gameicons/PNG/White/1x/forward.png"
		)
		self.playAsPlantsText = Display('Play As Plants', self.screen, (140, 100), 24, (0, 255, 0));

		self.playAsZombiesButton = Sprite(
			self.screen, (260, 200 - 20), (1, 1), "Assets/gameicons/PNG/White/1x/forward.png"
		)
		self.playAsZombiesText = Display('Play As Zombies', self.screen, (140, 200), 24, (125, 125, 125));

		self.usernameText = Display(self.dataManager.get('user_email'), self.screen, (200, 400), 12, (255, 255, 255));

		self.exitButton = Sprite(
			self.screen, (500, 400), (1, 1), "Assets/gameicons/PNG/White/1x/power.png"
		)

		# self.cancelButton = Sprite(self.screen, (400, 400), (1, 1), "Assets/gameicons/PNG/White/1x/power.png")

		self.loadingText = Display("Finding Match..", self.screen, (200, 240), 32, (255, 255, 255));

		self.spritesMenu.append(self.playAsPlantsButton)
		self.spritesMenu.append(self.playAsZombiesButton)
		self.spritesMenu.append(self.playAsPlantsText)
		self.spritesMenu.append(self.playAsZombiesText)
		self.spritesMenu.append(self.exitButton)
		self.spritesMenu.append(self.usernameText)

		# self.spritesLoading.append(self.cancelButton)
		self.spritesLoading.append(self.loadingText)

		self.try_disconnect_match()

	def events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.gameManager.running = False

			if self.state == 'MENU':
				if self.eventManager.checkOnClick(event, self.playAsPlantsButton):
					print("play game as plants")
					self.playGameAsPlants()
				elif self.eventManager.checkOnClick(event, self.playAsZombiesButton):
					print("play game as plants")
					self.playGameAsZombies()
				elif self.eventManager.checkOnClick(event, self.exitButton):
					print("exit game")
					self.exitGame()
			elif self.state == 'LOADING':
				pass
				# if self.eventManager.checkOnClick(event, self.cancelButton):
					# print("cancel game")
					# self.cancelGame()

	def render(self):
		self.screen.fill((0, 0, 0))
		self.screen.blit(self.bg,(0,0))

		if self.state == 'MENU':
			for sprite in self.spritesMenu:
				sprite.render()
		elif self.state == 'LOADING':
			for sprite in self.spritesLoading:
				sprite.render()

		self.update()

	def update(self):
		if self.will_find_match:
			if self.find_match_timer > 0:
				self.find_match_timer -= 1
			else:
				self.will_find_match = False
				self.find_match_timer = 60
				self.try_find_match(self.token, self.role)

	def playGameAsPlants(self):
		# self.gameManager.loadScene("LobbyMenu")
		self.state = 'LOADING'
		
		self.token = self.dataManager.get('user_token')
		self.role = 'plant'

		# self.try_find_match(token, role)
		self.will_find_match = True
		self.find_match_timer = 60

	def playGameAsZombies(self):
        # self.gameManager.loadScene("LobbyMenu")
		self.state = 'LOADING'

		self.token = self.dataManager.get('user_token')
		self.role = 'zombie'

		# self.try_find_match(token, role)
		self.will_find_match = True
		self.find_match_timer = 60

	def exitGame(self):
		self.gameManager.running = False

	def cancelGame(self):
		self.state = 'MENU'

	def find_match(self, token, role):
		if self.gameManager.accountSocket != None:
			res = self.gameManager.accountSocket.sendFindMatchEvent(token, role)

			return res
		return None

	def try_find_match(self, token, role):
		ne = self.find_match(token, role);
		print(ne)
		if ne['success'] and ne['match_status'] == 'waiting':
			anotherNe = self.gameManager.socketManager.receive()
			print(anotherNe)

		self.dataManager.set('user_token', token)
		self.dataManager.set('user_role', role)

		self.gameManager.loadScene('GameplayScene');

	def try_cancel_match(self):
		if self.dataManager.get('user_role'):
			token = self.dataManager.get('user_token')
			role = self.dataManager.get('user_role')

			self.gameManager.accountSocket.sendCancelFindMatchEvent(token, role)

	def try_disconnect_match(self):
		if self.dataManager.get('user_role'):
			self.gameManager.socketManager.close()
			self.gameManager.socketManager.connect()

			email_input = self.dataManager.get('user_email')
			password_input = self.dataManager.get('user_password')

			res = self.gameManager.accountSocket.sendAccountLoginEvent(email_input, password_input)
			token = res['token']

			self.dataManager.set('user_token', token)