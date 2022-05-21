import pygame

class GameManager():
	def __init__(self, dataManager, screenSize):
		pygame.init()
		
		self.screen = pygame.display.set_mode(screenSize)
		self.dataManager = dataManager
		self.scene = None

		self.running = True

	def loadScene(self, sceneClass):
		if sceneClass:
			self.scene = sceneClass(self)

	def run(self):
		while self.running:
			if self.scene is not None:
				self.scene.events()
				self.scene.render()

			pygame.display.flip()

		pygame.quit()
		