import pygame

class DataManager():
	def __init__(self):
		self.data = {}

	def get(self, key):
		if key in self.data:
			return self.data[key];
		return ''

	def set(self, key, value):
		self.data[key] = value
		