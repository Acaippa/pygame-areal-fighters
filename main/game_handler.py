import pygame
from menus.main_menu import*
from levels.main_game import*

class GameHandler:
	def __init__(self):
		self.delta_time = 0

		self.state = "mainmenu"

		self.main_menu = MainMenu(self)
		self.main_game = MainGame(self)


		self.states = {
		"mainmenu" : self.main_menu.update,
		"maingame" : self.main_game.update,
		}

	def change_state(self, state):
		self.state = state

	def run(self, delta_time):
		self.delta_time = delta_time

		# Run the correct state
		self.states.get(self.state)(self.delta_time)