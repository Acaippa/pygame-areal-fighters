import pygame
from math import*

class Bullet:
	def __init__(self, pos, angle, list):
		self.display_surface = pygame.display.get_surface()
		self.pos = pos

		self.image = pygame.Surface((10, 5), pygame.SRCALPHA)
		self.rect = self.image.get_rect()
		self.image.fill("yellow")

		self.speed = 3000

		self.last_x, self.last_y = 0, 0

		self.distance_traveled = 0

		self.delta_time = 0

		self.angle = angle

		self.list = list

	def get_speed(self):
		return self.distance_traveled * 60

	def kill_out_of_bounds(self):
		w, h = self.display_surface.get_size()
		try:
			if self.pos[0] >= w or self.pos[0] <= 0:
				self.list.remove(self)

			if self.pos[1] >= h or self.pos[1] <= 0:
				self.list.remove(self)
		except Exception as e:
			print("Failed to remove bullet; ", e)


	def update(self, dt):
		self.delta_time = dt

		self.kill_out_of_bounds()

		self.last_x, self.last_y = self.pos
		# We have to offset the angle by 90 degrees to sompensate for the fact that the 0 position for the barrel is at + 90 degrees.
		rad = radians(self.angle + 90)
		self.pos = self.pos[0] - (sin(rad) * self.speed * self.delta_time), self.pos[1] - (cos(rad) * self.speed * self.delta_time)

		self.distance_traveled = sqrt((self.pos[0] - self.last_x)**2 + (self.pos[1] - self.last_y)**2)

		self.image_rotated = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image_rotated.get_rect(center=self.pos)

		self.draw()

	def draw(self):
		self.display_surface.blit(self.image_rotated, self.rect)