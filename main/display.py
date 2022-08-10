import pygame
from game import*

class Display:
	def __init__(self):
		self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

		self.running = True
		self.clock = pygame.time.Clock()
		self.fps = 60

		self.game = Game()

		self.delta_tick = 0
		self.delta_time = 0

	def main_loop(self):
		while self.running:
			self.delta_tick = pygame.time.get_ticks()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.running = False

			self.game.run(self.delta_time)

			self.clock.tick(self.fps)

			self.delta_time = pygame.time.get_ticks() - self.delta_time

			pygame.display.flip()