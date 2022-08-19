import pygame
from settings import*
from modules.bullet import*
from math import*

class Turret:
	def __init__(self, pos, spawner):
		self.display_surface = pygame.display.get_surface()

		self.plane_spawner = spawner

		self.body = pygame.image.load("images/turretbody01.png").convert_alpha()
		w, h = self.body.get_size()
		self.body = pygame.transform.scale(self.body, (w*PLANE_SIZE, h*PLANE_SIZE))
		self.barrel = pygame.image.load("images/turretbarrel01.png").convert_alpha()
		w, h = self.barrel.get_size()
		self.barrel = pygame.transform.scale(self.barrel, (w*PLANE_SIZE, h*PLANE_SIZE))
		self.barrel_rotated = self.barrel
		self.barrel_rect = self.barrel.get_rect()

		self.delta_time = 0

		self.pos = pos

		# The offset needed for the barrel to stay at its correct place relative to teh gun body.
		self.offset_x = 25
		self.offset_y = 19

		self.angle = 0

		self.barrel_pos = (0, 0)

		self.shoot_delay = 0.1
		self.shoot_index = 0

		self.bullet_list = []

		self.target_plane = None

		self.target_bullet = None

	def update(self, dt):
		self.delta_time = dt

		if self.shoot_index >= self.shoot_delay:
			self.bullet_list.append(Bullet(self.barrel_pos, self.angle, self.bullet_list))
			self.shoot_index = 0
		else:
			self.shoot_index += 1 * self.delta_time

		self.aim()

		self.draw()

		self.draw_bullets()

	def get_bullets(self):
		return self.bullet_list

	def aim(self):
		self.target_plane = self.plane_spawner.get_first_plane()

		if self.target_plane != None:
			self.find_angle_to_enemy()

		self.barrel_rotated = pygame.transform.rotate(self.barrel, self.angle)
		self.barrel_rect = self.barrel_rotated.get_rect(center=self.barrel_pos)


	def find_angle_to_enemy(self):
		enemy_x, enemy_y = self.target_plane.rect.center

		bullet_speed = 0

		if self.target_bullet.get_speed() == 0:
			bullet_speed = 1
		else:
			bullet_speed = self.target_bullet.get_speed()

		distance = sqrt((self.pos[0] - enemy_x)**2 + (self.pos[0] - enemy_y)**2)
		offset = (distance / bullet_speed) * self.target_plane.get_speed()

		difference_x = self.pos[0] - (enemy_x - offset)
		difference_y = enemy_y - self.pos[1]

		self.angle = atan2(difference_y, difference_x)
		self.angle = degrees(self.angle)

	def draw_bullets(self):
		for bullet in self.bullet_list:
			bullet.update(self.delta_time)
			self.target_bullet = bullet

	def draw(self):
		x = self.pos[0] - self.body.get_width() // 2
		# Place the bottom of the turret at the position
		y = self.pos[1] - self.body.get_height()
		self.display_surface.blit(self.body, (x, y))

		self.barrel_pos = x + self.offset_x, y + self.offset_y
		self.display_surface.blit(self.barrel_rotated, self.barrel_rect)