import pygame

class CollisionHandler:
	def __init__(self, planes, bullets):
		self.display_surface = pygame.display.get_surface()
		for plane in planes:
			for bullet in bullets:
				collision = pygame.Rect.colliderect(plane.rect, bullet.rect)

				 # Check if the bullet hits the plane between frames.
				if collision:
					plane.on_collision()
					bullet.on_collision()