import pygame
from settings import*
from math import*

class Plane:
	def __init__(self, pos):
		self.display_surface = pygame.display.get_surface()
		self.image = pygame.image.load("images/plane01.png").convert_alpha()

		w, h = self.image.get_size()
		self.image = pygame.transform.scale(self.image, (w*PLANE_SIZE, h*PLANE_SIZE))

		self.pos = pos
		self.speed = 300

		self.delta_time = 0

		self.rect = self.image.get_rect()
		self.rect.center = self.pos

		self.last_x, self.last_y = 0, 0

		self.distance_traveled = 0


	def get_speed(self):
		return self.distance_traveled * 60

	def update(self, dt):
		self.delta_time = dt

		self.last_x, self.last_y = self.pos
		self.pos = self.pos[0] - self.speed * self.delta_time, self.pos[1]

		self.distance_traveled = hypot(self.last_x - self.pos[0], self.last_y - self.pos[1])

		self.draw()

	def draw(self):
		self.display_surface.blit(self.image, (self.pos[0] - self.rect.width // 2, self.pos[1] - self.rect.height // 2))