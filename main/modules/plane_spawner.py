import pygame
from modules.plane import*
import random

class PlaneSpawner:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

		self.plane_list = []

		self.planes = [
			Plane
		]

		self.plane_tick = 0

		self.delta_time = 0

		self.plane_timer = 5


	def get_first_plane(self):
		if len(self.plane_list) > 0:
			max = 0
			target = None
			for plane in self.plane_list:
				if plane.pos[0] < max or max == 0:
					max = plane.pos[0]
					target = plane
			return target
		else:
			return None

	def update(self, dt):
		self.delta_time = dt

		if self.plane_tick >= self.plane_timer:
			x = self.display_surface.get_width() + random.randint(50, 150)
			y = random.randint(200, 500)
			self.plane_list.append(random.choice(self.planes)((x, y)))
			self.plane_tick = 0

		else:
			self.plane_tick += 1 * self.delta_time

		self.draw()

	def draw(self):
		for plane in self.plane_list:
			if plane.pos[0] < 0:
				self.plane_list.remove(plane)
			else:
				plane.update(self.delta_time)