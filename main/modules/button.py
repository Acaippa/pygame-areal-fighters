import pygame
from PIL import ImageColor

class Button:
	def __init__(self, parent, text, pos, cmd, color="#ffffff", background="#222222", margin=10, **kwargs):
		if kwargs.get("surface", None) == None:
			self.display_surface = pygame.display.get_surface()
		else:
			self.display_surface = kwargs.get("surface", None)
		# self.font = pygame.font.SysFont('Segoe UI Normal', 40)
		self.font = pygame.font.Font('fonts/upheavtt.ttf', 40)

		parent.button_list.append(self)

		self.text = text
		self.color = color
		self.background_color = background
		self.pos = pos
		self.margin = margin
		self.hover = False
		self.cmd = cmd
		self.click_check = False

		self.highlight = 0

		self.edit = kwargs.get("edit", False)

		self.rendered_font = self.font.render(self.text, True, self.color)

		if pos[0] == "center":
			self.pos = self.display_surface.get_width() // 2, self.pos[1]

		self.get_custom_rect()

		self.move_amount_out = 50
		# Make the move index the negative half of the move amount. 
		self.move_index_out = -self.move_amount_out / 2

		self.move_amount_in = 50
		# Make the move index the negative half of the move amount. 
		self.move_index_in = -self.move_amount_in / 2

	def get_custom_rect(self):
		self.rect = self.rendered_font.get_rect()
		self.rect.width += self.margin * 2
		self.rect.height += self.margin
		self.rect.center = self.pos

	def update(self):
		self.on_hover()
		self.on_click()

		if self.edit:
			self.edit_move()

		self.rendered_font = self.font.render(self.text, True, self.color)
		self.draw()


	def hide_self(self, direction):
		if direction == "r":
			if self.move_index_out < self.move_amount_out:
				velocity = (-self.move_index_out ** 3) * 0.001
				self.pos = self.pos[0] + velocity, self.pos[1]
				self.move_index_out += 7


	def show_self(self, direction="r"):
		if direction == "r":
			if self.move_index_in < self.move_amount_in:
				velocity = (self.move_index_in ** 3) * 0.001
				self.pos = self.pos[0] + velocity, self.pos[1]
				self.move_index_in += 7



	def on_hover(self):
		mouse = pygame.mouse.get_pos()
		collide = self.rect.collidepoint(mouse)
		if collide:
			self.hover = True
			self.highlight = 50
		else:
			self.hover = False
			self.highlight = 0

	def edit_move(self): # Move the button with the arrows
		keys = pygame.key.get_pressed()

		spd = 1

		# Move faster
		if keys[pygame.K_LSHIFT]:
			spd = 10

		if keys[pygame.K_RIGHT]:
			self.pos = self.pos[0] + spd, self.pos[1]

		if keys[pygame.K_LEFT]:
			self.pos = self.pos[0] - spd, self.pos[1]

		if keys[pygame.K_UP]:
			self.pos = self.pos[0], self.pos[1] - spd

		if keys[pygame.K_DOWN]:
			self.pos = self.pos[0], self.pos[1] + spd

		self.rect.center = self.pos

	def on_click(self):
		pressed = pygame.mouse.get_pressed()

		if self.hover and pressed[0]:
			self.highlight = 100
			self.click_check = True

		if self.hover and pressed[0] == False and self.click_check:
			self.click_check = False

			# If the button is being placed for the first time we can click to show what its coords are.
			if self.edit:
				print(self.pos)

			try:
				self.cmd()
			except Exception as e:
				print(e)

		if self.hover == False:
			self.click_check = False

	def draw(self):
		self.get_custom_rect()

		rgbList = [0, 0, 0]

		rgbColor = ImageColor.getcolor(self.background_color, "RGB")

		# Check if the highlight value is above 255
		for i in range(len(rgbColor)):
			if rgbColor[i] + self.highlight > 255:
				rgbList[i] = 255
			else:
				rgbList[i] = rgbColor[i] + self.highlight

		pygame.draw.rect(self.display_surface, (rgbList[0], rgbList[1], rgbList[2]), self.rect, border_radius=5)
		self.display_surface.blit(self.rendered_font, (self.pos[0] - self.rendered_font.get_width()//2, self.pos[1] - self.rendered_font.get_height()//2))


# running = True

# display = pygame.display.set_mode((200, 200))
# pygame.font.init()
# button = Button("Gay homo", (100, 100), "wd")

# while running:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			running = False

# 		if event.type == pygame.KEYDOWN:
# 			if event.key == pygame.K_ESCAPE:
# 				running = False
# 	display.fill("#000000")
# 	button.update()
# 	pygame.display.flip()
