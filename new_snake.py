import pygame, random, sys


class Cube():
	def __init__(self, pos_x, pos_y):
		self.rect = pygame.Rect(pos_x, pos_y, 20, 20)

class Snake(Cube):
	def __init__(self, pos_x, pos_y, food):
		super().__init__(pos_x, pos_y)
		self.snake_cubes = [(pos_x, pos_y)]
		self.speed = 0
		self.food = food
		self.point = 0

	def move_up(self):
		self.speed += 4
		if self.speed == 20:
			self.speed = 0
			self.rect.y -= 20
			self.update()
		if self.rect.top < 0:
			self.rect.bottom = screen_height
			self.update()

	def move_down(self):
		self.speed += 4
		if self.speed == 20:
			self.speed = 0
			self.rect.y += 20
			self.update()
		if self.rect.bottom > screen_height:
			self.rect.top = 0
			self.update()

	def move_left(self):
		self.speed += 4
		if self.speed == 20:
			self.speed = 0
			self.rect.x -= 20
			self.update()
		if self.rect.left < 0:
			self.rect.right = screen_width
			self.update()

	def move_right(self):
		self.speed += 4
		if self.speed == 20:
			self.speed = 0
			
			self.rect.x += 20
			self.update()
		if self.rect.right > screen_width:
			self.rect.left = 0
			self.update()

	def eat(self):
		if self.rect.colliderect(self.food.rect):
			self.food.new_food()
			self.grown()
			self.point += 1

	def grown(self):
		self.snake_cubes.append(self.snake_cubes[len(self.snake_cubes)-1])

	def update(self):
		for index in reversed(range(len(self.snake_cubes))):
			if index != 0:
				self.snake_cubes[index] = self.snake_cubes[index - 1]
			else:
				self.snake_cubes[index] = (self.rect.x, self.rect.y)

class Food(Cube):
	def __init__(self,pos_x, pos_y):
		super().__init__(pos_x, pos_y)

	def new_food(self):
		lis_choice_x = range(int(screen_width/20))
		lis_choice_y = range(int(screen_height/20))
		self.rect.x = random.randint(0, screen_width/20 -1)*20
		self.rect.y = random.randint(0, screen_height/20 -1)*20

class Button():
	def __init__(self):
		self.position = [(screen_width/2 - 100, 100), (screen_width/2 - 100, 200), (screen_width/2 - 100, 300)]
		self.pos_count = 0

	def start_button(self, pos_count):
		x, y = self.position[pos_count]
		self.button_start = pygame.Rect(x, y, 200, 50)
		text_start = font.render("Start", True, bg_color)
		start_rect = text_start.get_rect(center=self.button_start.center)

		pygame.draw.rect(screen, snake_color, self.button_start)
		screen.blit(text_start, start_rect)

	def continue_button(self, pos_count):
		x, y = self.position[pos_count]
		self.button_continue = pygame.Rect(x, y, 200, 50)
		text_start = font.render("Continue", True, bg_color)
		start_rect = text_start.get_rect(center=self.button_continue.center)

		pygame.draw.rect(screen, snake_color, self.button_continue)
		screen.blit(text_start, start_rect)


	def highpoint_button(self, pos_count):
		x, y = self.position[pos_count]
		self.button_highpoint = pygame.Rect(x, y, 200, 50)
		text_start = font.render("High point", True, bg_color)
		start_rect = text_start.get_rect(center=self.button_highpoint.center)

		pygame.draw.rect(screen, snake_color, self.button_highpoint)
		screen.blit(text_start, start_rect)

class GameManager():
	def __init__(self, snake, food):
		self.snake = snake
		self.food = food
		self.direction = False

	def run_game(self):
		if self.direction == 'down':
			self.snake.move_down()
		if self.direction == 'up':
			self.snake.move_up()
		if self.direction == 'right':
			self.snake.move_right()
		if self.direction == 'left':
			self.snake.move_left()

		self.snake.eat()
		i = 0
		for a, b in self.snake.snake_cubes:
			rect_i = pygame.Rect(a, b, 20, 20)
			pygame.draw.rect(screen, snake_color, rect_i)
			
			if i > 1:
				if self.snake.rect.colliderect(rect_i):
					self.end_game()
					end_menu()
			i += 1
		pygame.draw.rect(screen, snake_color, self.snake.rect)
		pygame.draw.rect(screen, food_color, self.food.rect)
		point = font.render(str(self.snake.point), True, snake_color)
		point_rect = point.get_rect(center = (screen_width/2, 20))
		screen.blit(point, point_rect)

	def end_game(self):
		self.direction = False
		self.snake.point = 0
	def reset_game(self):
		self.direction = 'right'
		self.snake.snake_cubes = [(screen_width/2, screen_height/2)]
		self.snake.rect.x = screen_width/2
		self.snake.rect.y = screen_height/2
		self.snake.point = 0

def main_menu():
	click = False
	main_button = Button()
	while True:

		mx, my = pygame.mouse.get_pos()

		screen.fill(bg_color)
		main_button.start_button(0)
		main_button.highpoint_button(1)


		if main_button.button_start.collidepoint((mx, my)):
			if click:
				game_manager.direction = 'right'
				game()

		if main_button.button_highpoint.collidepoint((mx, my)):
			if click:
				hightpoint()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.flip()
		clock.tick(30)

def pause_menu():
	pause_button = Button()
	click = False
	while True:

		mx, my = pygame.mouse.get_pos()

		screen.fill(bg_color)

		pause_button.start_button(0)
		pause_button.continue_button(1)
		pause_button.highpoint_button(2)

		if pause_button.button_continue.collidepoint((mx, my)):
			if click:
				game()

		if pause_button.button_start.collidepoint((mx, my)):
			if click:
				game_manager.reset_game()
				game()

		if pause_button.button_highpoint.collidepoint((mx, my)):
			if click:
				hightpoint()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.flip()
		clock.tick(30)

def end_menu():
	click = False
	end_button = Button()
	while True:

		mx, my = pygame.mouse.get_pos()

		screen.fill(bg_color)

		end_button.start_button(0)
		end_button.highpoint_button(1)

		if end_button.button_start.collidepoint((mx, my)):
			if click:
				game_manager.reset_game()
				game()

		if end_button.button_highpoint.collidepoint((mx, my)):
			if click:
				hightpoint()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.flip()
		clock.tick(30)
	pass

def game():
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause_menu()
				if event.key == pygame.K_DOWN and game_manager.direction != 'up':
					game_manager.direction = 'down'
				if event.key == pygame.K_UP and game_manager.direction != 'down':
					game_manager.direction = 'up'
				if event.key == pygame.K_RIGHT and game_manager.direction != 'left':
					game_manager.direction = 'right'
				if event.key == pygame.K_LEFT and game_manager.direction != 'right':
					game_manager.direction = 'left'

		# Draw backgroup
		screen.fill(bg_color)

		if game_manager.direction:
			game_manager.run_game()


		pygame.display.flip()
		clock.tick(30)

def hightpoint():
	pass

# General set_up
pygame.init()
clock = pygame.time.Clock()

# Game Display
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# some color and font
snake_color = (200, 200, 200)
food_color = (200, 0, 0)
bg_color = pygame.Color('Grey12')
font = pygame.font.Font('freesansbold.ttf', 24)

# first food position
food_x = random.randint(0, screen_width/20 -1)*20
food_y = random.randint(0, screen_height/20 -1)*20
food = Food(food_x, food_y)

snake = Snake(screen_width/2, screen_height/2, food)


game_manager = GameManager(snake, food)

# Enter the game memu
main_menu()