import pygame
from settings import*
from modules.plane_spawner import*
from modules.turret import*
from modules.collision_handler import*

class MainGame:
	def __init__(self, parent):
		self.display_surface = pygame.display.get_surface()

		self.parent = parent

		w, h = self.display_surface.get_size()
		self.background_image = pygame.image.load("images/field.png").convert_alpha()
		self.background_image = pygame.transform.scale(self.background_image, (w, h))

		self.ground_tile = pygame.image.load("images/ground.png").convert_alpha()
		self.ground_tile = pygame.transform.scale(self.ground_tile, (TILE_SIZE, TILE_SIZE))

		self.plane_spawner = PlaneSpawner()

		self.turret = Turret((1000, self.display_surface.get_height() - self.ground_tile.get_height()), self.plane_spawner)

	def update(self, dt):
		self.delta_time = dt
		self.draw_background()

		CollisionHandler(self.plane_spawner.get_planes(), self.turret.get_bullets())

		self.plane_spawner.update(self.delta_time)

		self.turret.update(self.delta_time)

		self.draw()

	def draw_background(self):
		self.display_surface.blit(self.background_image, (0, 0))

		for i in range((self.display_surface.get_width() // TILE_SIZE) + 1):
			self.display_surface.blit(self.ground_tile, (i * TILE_SIZE, self.display_surface.get_height() - self.ground_tile.get_height()))

	def draw(self):
		pass
