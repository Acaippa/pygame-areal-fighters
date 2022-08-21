import pygame
from modules.button import*

class ShopMenu:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.margin = 20
		w, h = self.display_surface.get_size()
		self.surface = pygame.Surface((w/5, h-self.margin*2))
		self.width, self.height = self.surface.get_size()

		self.pos = -self.width, self.margin

		self.velocity = 1000

		self.delta_time = 0

		self.button_list = []

		self.close_button = Button(self, "X", (354, 31), "d", surface=self.surface)

	def show_self(self, direction):
		if direction == "r":

			if self.pos[0] + self.velocity * self.delta_time < 0:
				self.pos = self.pos[0] + self.velocity * self.delta_time, self.pos[1]

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		self.surface.fill('#000000')

		for i in self.button_list:
			i.update()

		self.display_surface.blit(self.surface, self.pos)