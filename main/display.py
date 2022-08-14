import pygame
from game_handler import*

class Display:
	def __init__(self):
		self.display_surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
		
		pygame.init()
		pygame.font.init()
		pygame.mixer.init()

		self.running = True
		self.clock = pygame.time.Clock()
		self.fps = 60

		self.game = GameHandler()

		self.delta_time = 0

	def main_loop(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.running = False

			self.display_surface.fill("#ffffff")

			self.game.run(self.delta_time)

			self.delta_time = self.clock.tick(self.fps) / 1000

			pygame.display.update()