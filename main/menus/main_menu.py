import pygame
from modules.button import*

class Menu:
	def __init__(self, parent):
		self.display_surface = pygame.display.get_surface()

		self.button_list = []
		self.background_image = None

		# The game_handler
		self.parent = parent

		self.delta_time = 0

	def update(self, dt):
		self.delta_time = dt

		self.draw()

	def draw(self):
		if self.background_image != None:
			self.display_surface.blit(self.background_image, (0, 0))

		for button in self.button_list:
			button.update()

class MainMenu(Menu):
	def __init__(self, parent):
		super().__init__(parent)
		
		self.background_image = pygame.image.load("images/field.png")
		w, h = self.display_surface.get_width(), self.display_surface.get_height()
		self.background_image = pygame.transform.scale(self.background_image, (w, h))

		self.play_button = Button(self, "Start new game", ("center", 400), lambda: self.parent.change_state("maingame"))

