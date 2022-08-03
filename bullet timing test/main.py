import pygame
from math import*
# Figure out a way to make the enemies predict the offset needed in order to hit fast mobing planes.

class Enemy:
	"""
	Follows the mouse cursor and returns its speed in pixels per second to the shooter
	"""
	def __init__(self):
		self.display = pygame.display.get_surface() # Get the pygame screen so we can blit to it
		self.pos = pygame.mouse.get_pos() # Set the initial position of the enemy to be the mouse position
		# Make a red square for the Enemy
		self.surface = pygame.Surface((25, 25))
		self.surface.fill("red")
		# Get the Rect of the surface so we can use it for collisions and size etc.
		self.rect = self.surface.get_rect()

		self.last_x = 0
		self.last_y = 0

	def update(self): # Update its variables and draw
		# Move the Enemy with the cursor
		self.pos = pygame.mouse.get_pos()

		self.get_speed()
		self.draw()

	def draw(self): # Draw the object
		self.display.blit(self.surface, (self.pos[0] - (self.rect.width // 2), self.pos[1] - (self.rect.height // 2)))

	def get_speed(self): # Return its speed
		target = pygame.math.Vector2(self.pos[0], self.pos[1])
		start = pygame.math.Vector2(self.last_x, self.last_y)
		self.last_x, self.last_y = self.pos

		delta = target - start
		print(delta)


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



	def update(self): # Update its variables and draw
		if self.shoot_index < self.shoot_delay: # Shoot 
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
			if bullet.is_out_of_bounds():
				self.bullet_list.remove(bullet)
			else:
				bullet.update()

	def get_angle_to_enemy(self): # Get the angle between the enemy and the shooter
		# Calculate the difference between both the objects axi
		difference_x = self.enemy.pos[0] - self.pos[0] 
		difference_y = self.enemy.pos[1] - self.pos[1]
		# Plug the difference into this function 
		angle = atan2(difference_y, difference_x)
		# Convert to angle
		angle = degrees(angle)
		return angle

	def draw(self): # Draw the object
		# Centering the object in both axis by subtracting half of its with from its position
		self.display.blit(self.surface, (self.pos[0] - (self.rect.width // 2), self.pos[1] - (self.rect.height // 2)))


class Bullet:
	"""
	Gets shot by the shooter and its speed is used to determine the offset needed to hit the enemy
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
		self.speed = 15

		self.last_x = 0
		self.last_y = 0

	def update(self): # Update its variables and draw
		# Use Cos and Sin to determine what proportion to move in pixels in otder to move in a cerain angle by inputting the angle in radians
		angle_in_radians = radians(self.angle)
		self.pos = (self.pos[0] + (self.speed * cos(angle_in_radians)), self.pos[1] + (self.speed * sin(angle_in_radians)))

		self.get_speed()
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

	def get_speed(self): # Return its speed
		target = pygame.math.Vector2(self.pos[0], self.pos[1])
		start = pygame.math.Vector2(self.last_x, self.last_y)
		self.last_x, self.last_y = self.pos

		delta = target - start
		print(delta)




pygame.init()

screen = pygame.display.set_mode((1000, 600)) # Setting the screen dimentions in pixels

running = True # Variable used for tracking if the user has closed the program

enemy = Enemy()
shooter = Shooter(enemy) # Give the shooter a reference of the enemy instance so it can retreive the speed from the enemy.

# Clock used later for limiting framarate
clock = pygame.time.Clock()

while running: # Main game loop
	for event in pygame.event.get(): # Check if the user has pressed the exit button
		if event.type == pygame.QUIT:
			running = False

	screen.fill("black") # Reset the screen color

	shooter.update()
	enemy.update()

	clock.tick(60)
	pygame.display.flip() # Update the display