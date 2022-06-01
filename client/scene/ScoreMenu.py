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
        self.dataManager.set('game_winner', 'zombie')
        self.status = self.dataManager.get('game_winner')

        self.awake()
        self.awakeScore()

    def awake(self):
        if (self.status == 'plant'):
            self.state = 'PLANT'
        elif (self.status == 'zombie'):
            self.state = 'ZOMBIE'

        self.lobbyButton = Sprite(
            self.screen, (200,300), (1,1), "Assets/gameicons/PNG/White/1x/power.png"
        )
        self.mainMenuButton = Sprite(
            self.screen, (500,300), (1,1), "Assets/gameicons/PNG/White/1x/power.png"
        )

        print("masuk awake")

        self.sprites[self.state].append(self.lobbyButton)
        self.sprites[self.state].append(self.mainMenuButton)


    def awakeScore(self):
        print("masuk awakeScore")
        
        self.object['score'] = Display (
            'Congratulation!', self.screen, (400,100), 52, color='white'
        )
        
        if self.state is 'PLANT':
            self.object['scoreWinner'] = Display (
                (self.state + ' Winner!'), self.screen, (400,200), 48, color='green'
            )

        else:
            self.object['scoreWinner'] = Display (
                (self.state + ' Winner!'), self.screen, (400,200), 48, color='grey'
            )
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quiting the Game")
                self.exitGame()
            if self.eventManager.checkOnClick(event, self.lobbyButton):
                print("going back to Lobby.")
                self.backToLobby()
            elif self.eventManager.checkOnClick(event, self.mainMenuButton):
                print("going back to main menu...")
                self.goToMainMenu()

    def render(self):
        self.screen.fill((0, 0, 0)) 
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