import pygame

class DataManager():
	def __init__(self):
		self.data = {}

	def get(self, key):
		return self.data[key];

	def set(self, key, value):
		self.data[key] = value
		