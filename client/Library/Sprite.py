import pygame

class Sprite():
	def __init__(self, screen, position, scale, imageSrc):
		super().__init__()

		self.screen = screen # gameManager.screen
		self.position = position # (x, y)
		self.scale = scale # (x, x)
		self.imageSrc = imageSrc # url
		self.image = pygame.image.load(imageSrc) # image
		self.imageRenderOriginal = self.image.convert_alpha() # png
		self.imageRender = self.imageRenderOriginal

		self.setDirty()

	def setPosition(self, pos):
		self.position = pos
		self.setDirty()

	def setScale(self, scale):
		self.scale = scale
		self.setDirty()

	def setDirty(self):
		width = self.image.get_width() * self.scale[0]
		height = self.image.get_height() * self.scale[1]
		transform = (int(width), int(height))
		self.imageRender = pygame.transform.scale(self.imageRender, transform)

	def render(self):
		self.screen.blit(self.imageRender, (self.position[0], self.position[1]))