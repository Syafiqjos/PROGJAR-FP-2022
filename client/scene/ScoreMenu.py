import sys
sys.path.append('..')

from Library.Sprite import Sprite
from Library.Display import Display

import pygame

class ScoreMenu(): 
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.dataManager = self.gameManager.dataManager 
        self.eventManager = self.gameManager.eventManager 
        self.screen = self.gameManager.screen 
        self.sprites = {'SCORE': [], 'PLANT': [], 'ZOMBIE': []}
        self.object = {}
        self.bg = pygame.image.load('Assets/our/plants-vs-zombies-wallpaper.jpg')
        self.bg = pygame.transform.scale(self.bg,(720,480))
        # self.dataManager.set('game_winner', 'zombie')
        # self.status = self.dataManager.get('user_role')
		# self.winner = self.dataManager.get('user_winner')
        self.status = self.dataManager.get('user_winner')
        self.role = self.dataManager.get('user_role')

        self.awake()
        self.awakeScore()

    def awake(self):
        if (self.role == 'plant'):
            self.state = 'PLANT'
        elif (self.role == 'zombie'):
            self.state = 'ZOMBIE'

        # self.lobbyButton = Sprite(
            # self.screen, (200,300), (1,1), "Assets/gameicons/PNG/White/1x/power.png"
        # )
        self.mainMenuButton = Sprite(
            self.screen, (720/2,300), (2,2), "Assets/gameicons/PNG/White/1x/power.png"
        )

        print("masuk awake")

        # self.sprites[self.state].append(self.lobbyButton)
        self.sprites[self.state].append(self.mainMenuButton)


    def awakeScore(self):
        print("masuk awakeScore")

        print('winner is', self.status)
        
        if self.status == 'plant' and self.state == 'PLANT' or self.status == 'zombie' and self.state == 'ZOMBIE':
                self.object['score'] = Display (
                    'Congratulation!', self.screen, (380,100), 52, color=(255, 255, 255)
                )
        else:
                self.object['score'] = Display (
                    'You Lose!', self.screen, (380,100), 52, color=(255, 0, 0)
                )
        
        if self.status is 'plant':
            self.object['scoreWinner'] = Display (
                ('PLANT Winner!'), self.screen, (380,200), 48, color=(0, 255, 0)
            )

        else:
            self.object['scoreWinner'] = Display (
                ('ZOMBIE Winner!'), self.screen, (380,200), 48, color=(125, 125, 125)
            )
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quiting the Game")
                self.exitGame()
            # if self.eventManager.checkOnClick(event, self.lobbyButton):
                # print("going back to Lobby.")
                # self.backToLobby()
            elif self.eventManager.checkOnClick(event, self.mainMenuButton):
                print("going back to main menu...")
                self.goToMainMenu()

    def render(self):
        self.screen.fill((0, 0, 0)) 
        self.screen.blit(self.bg,(0,0))
        # print("masuk re")
        for sprite in self.sprites[self.state]:
            # print("masuk render2")
            self.object['score'].awake()
            self.object['scoreWinner'].awake()
            sprite.render()

    def backToLobby(self):
        self.gameManager.loadScene('LobbyMenu')

    def goToMainMenu(self): 
        self.gameManager.loadScene('MainMenu')

    def exitGame(self):
        self.gameManager.running = False