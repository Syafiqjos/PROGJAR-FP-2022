import pygame

class GameManager():
	def __init__(self, dataManager, eventManager, screenSize):
		pygame.init()
		
		self.screen = pygame.display.set_mode(screenSize)
		self.dataManager = dataManager
		self.eventManager = eventManager
		self.scenes = {}
		self.scene = None
		self.clock = pygame.time.Clock()

		self.running = True

	def registerScene(self, sceneName, sceneClass):
		self.scenes[sceneName] = sceneClass

	def loadScene(self, sceneName):
		sceneClass = self.scenes[sceneName]
		if sceneClass:
			self.scene = sceneClass(self)
		else:
			print('Loading Scene Error')

	def run(self):
		while self.running:
			if self.scene is not None:
				self.scene.events()
				self.scene.render()

			pygame.display.flip()
			self.clock.tick(60)

		pygame.quit()
		