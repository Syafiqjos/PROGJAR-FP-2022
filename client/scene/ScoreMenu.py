import sys
sys.path.append('..')

from Library.Sprite import Sprite
from Library.Display import Display

import pygame

class ScoreMenu(): 
    def __init__(self, gameManager, status):
        self.gameManager = gameManager
        self.dataManager = self.gameManager.dataManager 
        self.eventManager = self.gameManager.eventManager 
        self.screen = self.gameManager.screen 
        self.sprites = {'SCORE': [], 'PLANT': [], 'ZOMBIE': []}
        self.object = {}
        self.status = status

        self.awake()
        self.awakeScore(status)

    def awake(self):
        self.state = 'SCORE'

        self.object = Sprite(
            self.screen, (200,300), (1,1), "Assets/gameicons/PNG/White/1x/power.png"
        )
        self.mainMenuButton = Sprite(
            self.screen, (500,300), (1,1), "Assets/gameicons/PNG/White/1x/power.png"
        )

        self.sprites[self.state].append(self.lobbyButton)
        self.sprites[self.state].append(self.mainMenuButton)

    def awakeScore(self, status):
        if (status):
            self.state = 'PLANT'
        else:
            self.state = 'ZOMBIE'
        
        self.object.score = Display (
            'Congratulation!', self.screen, (300,100), 48, (255,255,255)
        )
    
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