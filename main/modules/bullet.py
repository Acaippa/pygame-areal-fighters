import pygame
from math import*

class Bullet:
	def __init__(self, pos, angle):
		self.display_surface = pygame.display.get_surface()
		self.pos = pos

		self.image = pygame.Surface((10, 5), pygame.SRCALPHA)
		self.rect = self.image.get_rect()
		self.image.fill("yellow")

		self.speed = 2500

		self.last_x, self.last_y = 0, 0

		self.distance_traveled = 0

		self.delta_time = 0

		self.angle = angle

	def get_speed(self):
		return self.distance_traveled * 60

	def update(self, dt):
		self.delta_time = dt

		self.last_x, self.last_y = self.pos
		# We have to offset the angle by 90 degrees to sompensate for the fact that the 0 position for the barrel is at + 90 degrees.
		rad = radians(self.angle + 90)
		self.pos = self.pos[0] - (sin(rad) * self.speed * self.delta_time), self.pos[1] - (cos(rad) * self.speed * self.delta_time)

		self.distance_traveled = hypot(self.last_x - self.pos[0], self.last_y - self.pos[1])

		self.image_rotated = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image_rotated.get_rect(center=self.pos)

		self.draw()

	def draw(self):
		self.display_surface.blit(self.image_rotated, self.rect)