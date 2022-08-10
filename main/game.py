import pygame

class Game:
	def __init__(self):
		self.delta_time = 0

	def run(self, delta_time):
		self.delta_time = delta_time