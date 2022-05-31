import sys
sys.path.append('..')

from Library.Sprite import Sprite

import pygame

class ScoreMenu(): 
    def __init__(self, gamManager):
        self.gameManager = gameManager
        self.dataManager = self.gameManager.dataManager 
        self.eventManager = self.gameManager.eventManager 
        self.screen = self.gameManager.screen 
        self.sprites = []

        self.awake()

    def awake(self):
        self.state = 'SCORE'

        self.lobbyButton = Sprite(
            self.screen, (100,100), (1,1), "Assets/gameicons/PNG/White/1x/power.png"
        )
        self.mainMenuButton = Sprite(
            self.screen, (300,300), (1,1), "Assets/gameicons/PNG/White/1x/power.png"
        )

        self.sprites.append(self.lobbyButton)
        self.sprites.append(self.mainMenuButton)

    def awakeScore(self):
        pass
    
    def event(self):
        for event in pygames.event.get():
            if event.type == pygame.QUIT:
                print("Quiting the Game")
                self.exitGame()
            if self.eventManager.checkOnClick(event, self.lobbyButton):
                print("going back to Lobby.")
                self.backToLobby()
            elif self.eventManager.checkOnClick(event, self.mainMenuButtom):
                print("going back to main menu...")
                self.goToMainMenu()


    def backToLobby(self):
        self.gameManager.loadScene('LobbyMenu')

    def goToMainMenu(self): 
        self.gameManager.loadScene('MainMenu')

    def exitGame(self):
        self.gameManager.running = False