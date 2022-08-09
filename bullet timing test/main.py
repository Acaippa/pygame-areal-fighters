import pygame
from math import*
import random
# Figure out a way to make the enemies predict the offset needed in order to hit fast mobing planes.

class Enemy:
	"""
	Follows the mouse cursor and returns its speed in pixels per second to the shooter
	"""
	def __init__(self):
		self.display = pygame.display.get_surface() # Get the pygame screen so we can blit to it
		self.pos = (10, 50)
		# Make a red square for the Enemy
		self.surface = pygame.Surface((25, 25))
		self.surface.fill("red")
		# Get the Rect of the surface so we can use it for collisions and size etc
		self.rect = self.surface.get_rect()
		# Time between frames used for speed calculation
		self.dt = 0
		# The velocity of the enemy and the direction its traveling
		self.xVel = 500
		self.xDir = 1
		# Variables that will be used to store the last position of the enemy so we can later calculate its speed
		self.last_x = 0
		self.last_y = 0
		# The length traveled between each frame
		self.length_traveled = 0

	def update(self, dt): # Update its variables and draw
		self.dt = dt

		# Whenever the enemy hits any of the sides of the screen, we invert its velocity and and xDir variable indicating in which direction the enemy is traveling
		if self.pos[0] >= self.display.get_width() or self.pos[0] < 0:
			self.xVel *= -1
			self.xDir *= -1

		# Before updating the position of the enemy we save its previous position so we can use the difference between the two to figure out the speed
		self.last_x, self.last_y = self.pos
		self.pos = (self.pos[0] + (self.xVel * self.dt), self.pos[1])

		# Get the length that the enemy has traveled in a frame
		self.length_traveled = sqrt((self.pos[0] - self.last_x)**2 + (self.pos[1] - self.last_y)**2)

		self.draw()

	def draw(self): # Draw the object
		# Subtract the position with half of the rect width to center the object
		self.display.blit(self.surface, (self.pos[0] - (self.rect.width // 2), self.pos[1] - (self.rect.height // 2)))

	def get_speed(self): # Return its speed in pixels / second
		return self.length_traveled * 60


class Shooter:
	"""
	Stays at the same place and fires at the enemy with an offset determined by the speed of the enemy
	"""
	def __init__(self, enemy):
		self.display = pygame.display.get_surface() # Get the pygame screen so we can blit to it 
		self.enemy = enemy
		self.pos = (self.display.get_size()[0] // 2, self.display.get_size()[1] - 50) # Set the position of the shooter to the middle of the screen in the X axis
		# Create a green square to visualize the position of the shooter
		self.surface = pygame.Surface((20, 20))
		self.surface.fill("green")
		# Get the Rect of the surface so we can use it for collisions and size etc.
		self.rect = self.surface.get_rect()
		# Variables controlling the time between shots
		self.shoot_delay = 10
		self.shoot_index = 0
		# List of all bullets on screen
		self.bullet_list = []
		# Angle of the gun
		self.angle = 0
		# The bullet we later will use to calculate the needed offset to hit the enemy
		self.target_bullet = None
		# The time between frames, used for speed calculations later in the code
		self.dt = 0


	def update(self, dt): # Update its variables and draw
		self.dt = dt
		# Shoot at an interval
		if self.shoot_index < self.shoot_delay: 
			self.shoot_index += 1
		else:
			self.shoot_index = 0
			self.shoot()

		self.angle = self.get_angle_to_enemy()
		self.update_bullets()	
		self.draw()

	def shoot(self):
		self.bullet_list.append(Bullet(self.pos, self.angle))

	def update_bullets(self):
		for bullet in self.bullet_list:
			self.target_bullet = bullet
			if bullet.is_out_of_bounds():
				self.bullet_list.remove(bullet)
			else:
				bullet.update(self.dt)

	def get_angle_to_enemy(self): # Get the angle between the enemy and the shooter
		# When the target bullet is None it typically means that the gun hasnt shot any bullets yet, so we just set the bullet speed to some arbitrary value, making sure its not 0 as to prevent division of 0 later in the code.
		if self.target_bullet != None and self.target_bullet.get_speed() != 0:
			bullet_speed = self.target_bullet.get_speed()
		else:
			bullet_speed = 1

		distance = sqrt((self.pos[0] - self.enemy.pos[0])**2 + (self.pos[0] - self.enemy.pos[1])**2)

		# Calculate the proper angle to aim by calculating the distance the enemy will move in the time the bullet takes to travel the distance between the shooter and the enemy.
		# The reason for the enemy.xDir variable is due to the offset only being applied in one direction, so when the enemy turns around, the direction needs to be multiplied negatively or posetively according to the x axis direction of the enemy so the bullet will hit properly
		difference_x = self.enemy.pos[0] + self.enemy.rect.width // 2 * self.enemy.xDir + ((distance / bullet_speed) * self.enemy.get_speed()) * self.enemy.xDir - self.pos[0] 
		difference_y = self.enemy.pos[1] + self.enemy.rect.height // 2 - self.pos[1]
		# Plug the difference into this function to get the radians
		angle = atan2(difference_y, difference_x)
		# Convert the radians into an angle and return it
		angle = degrees(angle)
		return angle

	def draw(self): # Draw the object
		# Centering the object in both axis by subtracting half of its with from its position
		self.display.blit(self.surface, (self.pos[0] - (self.rect.width // 2), self.pos[1] - (self.rect.height // 2)))


class Bullet:
	"""
	Gets shot out by the shooter and its speed is used to determine the offset needed to hit the enemy
	"""
	def __init__(self, pos, angle):
		self.display = pygame.display.get_surface() # Get the pygame screen so we can blit to it
		self.pos = pos
		# Create a yellow rectangle for the bullet body
		self.surface = pygame.Surface((20, 15))
		self.surface.fill("yellow")
		# Get the rect of the surface for collision and height and width control
		self.rect = self.surface.get_rect()
		# The angle the bullet will travel at
		self.angle = angle
		# The speed at which the bullet will travel at
		self.speed = 1050
		# Parameters used later to calculate how far the bullet has moved every frame
		self.last_x = 0
		self.last_y = 0

	def update(self, dt): # Update its variables and draw
		# Use Cos and Sin to determine what proportion to move in pixels in otder to move in a cerain angle by inputting the angle in radians
		self.dt = dt

		# Convert the angle to radians so we can plot the radians into cos and sin functions to figure out at velocity in each axis the bullet has to move the move in the right angle
		angle_in_radians = radians(self.angle)
		self.last_x, self.last_y = self.pos
		self.pos = (self.pos[0] + (self.speed * cos(angle_in_radians) * self.dt), self.pos[1] + (self.speed * sin(angle_in_radians) * self.dt))

		self.length_traveled = sqrt((self.pos[0] - self.last_x)**2 + (self.pos[1] - self.last_y)**2)

		self.draw()

	def draw(self): # Draw the object
		# Center the bullet around its position
		self.display.blit(self.surface, (self.pos[0] - (self.rect.width // 2), self.pos[1] - (self.rect.height // 2)))

	def is_out_of_bounds(self):
		# Check if the bullet is outside of the screen
		if self.pos[0] > self.display.get_width() or self.pos[1] > self.display.get_height() or self.pos[0] < 0 or self.pos[1] < 0:
			return True
		else:
			return False

	def get_speed(self): # Return its speed in pixels / second
		print(self.length_traveled)
		return self.length_traveled * 60




pygame.init()

screen = pygame.display.set_mode((1000, 600)) # Setting the screen dimentions in pixels

running = True # Variable used for tracking if the user has closed the program

enemy = Enemy()
shooter = Shooter(enemy) # Give the shooter a reference of the enemy instance so it can retreive the speed from the enemy.

# Clock used later for limiting framarate
clock = pygame.time.Clock()

delta_tick = 0
delta_time = 0

while running: # Main game loop
	for event in pygame.event.get(): # Check if the user has pressed the exit button
		if event.type == pygame.QUIT:
			running = False

	delta_tick = pygame.time.get_ticks()

	screen.fill("black") # Reset the screen color

	shooter.update(delta_time)
	enemy.update(delta_time)

	clock.tick(60)
	delta_time = (pygame.time.get_ticks() - delta_tick) / 1000
	delta_tick = pygame.time.get_ticks()
	pygame.display.flip() # Update the display
