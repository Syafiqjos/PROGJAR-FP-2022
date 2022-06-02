import sys

sys.path.append("..")

from Library.Sprite import Sprite

import pygame


class MainMenu:
    def __init__(self, gameManager):
        self.gameManager = gameManager
        self.dataManager = self.gameManager.dataManager
        self.eventManager = self.gameManager.eventManager
        self.screen = self.gameManager.screen
        self.sprites = []

        self.awake()

    def awake(self):
        self.playButton = Sprite(
            self.screen, (100, 100), (1, 1), "Assets/gameicons/PNG/White/1x/forward.png"
        )
        self.exitButton = Sprite(
            self.screen, (300, 100), (1, 1), "Assets/gameicons/PNG/White/1x/power.png"
        )

        self.sprites.append(self.playButton)
        self.sprites.append(self.exitButton)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameManager.running = False
            if self.eventManager.checkOnClick(event, self.playButton):
                print("play game")
                self.playGame()
            elif self.eventManager.checkOnClick(event, self.exitButton):
                print("exit game")
                self.exitGame()

    def render(self):
        self.screen.fill((0, 0, 0))

        for sprite in self.sprites:
            sprite.render()

    def playGame(self):
        self.gameManager.loadScene("LobbyMenu")

    def exitGame(self):
        self.gameManager.running = False
