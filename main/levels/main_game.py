import pygame
from settings import*
from modules.plane_spawner import*
from modules.turret import*
from modules.collision_handler import*
from modules.button import*
from menus.shop_menu import*

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

		self.button_list = []

		self.hide_button_bool = False

		self.shop_button = Button(self, "shop", (77, 1041), self.activate_hide_button)

		self.shop_menu = ShopMenu()

	def activate_hide_button(self):
		self.hide_button_bool = True

	def update(self, dt):
		self.delta_time = dt
		self.draw_background()

		self.plane_spawner.update(self.delta_time)

		self.shop_menu.update(self.delta_time)

		self.shop_button.update()

		if self.hide_button_bool:
			self.shop_button.hide_self("r")
			self.shop_menu.show_self("r")

		self.draw()

	def draw_background(self):
		self.display_surface.blit(self.background_image, (0, 0))

		for i in range((self.display_surface.get_width() // TILE_SIZE) + 1):
			self.display_surface.blit(self.ground_tile, (i * TILE_SIZE, self.display_surface.get_height() - self.ground_tile.get_height()))

	def draw(self):
		pass
