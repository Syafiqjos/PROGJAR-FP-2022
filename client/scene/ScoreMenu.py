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
        self.sprites = { 'HOME': [], 'LOBBY': [], 'SCORE': [] }
        self.objects = {}
        
        self.awake()

    def awake(self):
        self.state = 'SCORE'
        
        self.awakeHome()
        self.awakeLobby()
        self.awakeScore()

    def awakeHome(self):
        #what happen

    def awakeLobby(self):
        #what happen

    def awakeScore(self):
        #what happen

    def backToLobby(self):
        self.gameManager.loadScene('LobbyMenu')

    def goToMainMenu(self):
		self.gameManager.loadScene('MainMenu')