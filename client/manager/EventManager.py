import pygame

class EventManager():
	def __init__(self):
		pass

	def checkOnClickAny(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			return True
		return False

	def checkOnClick(self, event, sprite):
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and sprite.rect.collidepoint(event.pos):
			return True
		return False
		