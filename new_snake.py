import pygame, random, sys
import json

class Cube(object):
	def __init__(self, pos_x, pos_y):
		self.rect = pygame.Rect(pos_x, pos_y, 20, 20)

class Snake(Cube):
	def __init__(self):
		pos_x = screen_width/2
		pos_y = screen_height/2
		self.rect = pygame.Rect(pos_x, pos_y, 20, 20)
		self.snake_cubes = [Cube(pos_x, pos_y)]
		self.speed = 0

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

	def grown(self):
		self.snake_cubes.append(self.snake_cubes[len(self.snake_cubes)-1])

	def update(self):
		for index in reversed(range(len(self.snake_cubes))):
			if index != 0:
				self.snake_cubes[index] = self.snake_cubes[index - 1]
			else:
				self.snake_cubes[index] = Cube(self.rect.x, self.rect.y)

class Food(Cube):
	def __init__(self):
		food_x = random.randint(0, screen_width/20 -1)*20
		food_y = random.randint(0, screen_height/20 -1)*20
		super().__init__(food_x, food_y)
	def new_food(self):
		lis_choice_x = range(int(screen_width/20))
		lis_choice_y = range(int(screen_height/20))
		self.rect.x = random.randint(0, screen_width/20 -1)*20
		self.rect.y = random.randint(0, screen_height/20 -1)*20

class Button():
	def __init__(self, pos_count, button_name):
		self.position = [(screen_width/2 - 100, 100), (screen_width/2 - 100, 200), (screen_width/2 - 100, 300)]
		self.pos_count = 0
		x, y = self.position[pos_count]
		self.rect = pygame.Rect(x, y, 200, 50)
		self.text = font.render(button_name, True, bg_color)
		self.text_rect = self.text.get_rect(center=self.rect.center)

	def draw_on_screen(self):
		pygame.draw.rect(screen, snake_color, self.rect)
		screen.blit(self.text, self.text_rect)

class GameManager(object):
	def __init__(self):
		self.snake = Snake()
		self.food = Food()
		self.direction = False
		self.point = 0

	def run_game(self):
		if self.direction == 'down':
			self.snake.move_down()
		if self.direction == 'up':
			self.snake.move_up()
		if self.direction == 'right':
			self.snake.move_right()
		if self.direction == 'left':
			self.snake.move_left()

		if self.snake.rect.colliderect(self.food.rect):
			self.food.new_food()
			self.snake.grown()
			self.point += 1
		
		for i, cube in enumerate(self.snake.snake_cubes):
			pygame.draw.rect(screen, snake_color, cube)
			
			
			if self.snake.rect.colliderect(cube) and i > 1:
				self.end_game()
				main_menu()
			
		pygame.draw.rect(screen, snake_color, self.snake.rect)
		pygame.draw.rect(screen, food_color, self.food.rect)
		point = font.render(str(self.point), True, snake_color)
		point_rect = point.get_rect(center = (screen_width/2, 20))
		screen.blit(point, point_rect)


	def end_game(self):
		print(self.point)
		with open('scores.json', 'r') as read_file:
			scores = json.load(read_file)
			scores['highScores'].append(self.point)
			scores['highScores'].sort(reverse=True)
		with open('scores.json', 'w') as write_file:
			json.dump(scores, write_file)

		self.direction = False
		self.point = 0

	def reset_game(self):
		self.direction = 'right'
		self.snake.snake_cubes = [Cube(screen_width/2, screen_height/2)]
		self.snake.rect.x = screen_width/2
		self.snake.rect.y = screen_height/2
		self.snake.point = 0

def main_menu():
	click = False
	start_button = Button(0, 'Start')
	high_score_button = Button(1, 'High score')
	while True:

		mx, my = pygame.mouse.get_pos()

		screen.fill(bg_color)
		start_button.draw_on_screen()
		high_score_button.draw_on_screen()

		if start_button.rect.collidepoint((mx, my)):
			if click:
				game_manager.reset_game()
				game()

		if high_score_button.rect.collidepoint((mx, my)):
			if click:
				high_score()

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
	start_button = Button(0, 'Start')
	continue_button = Button(1, 'Continue')
	high_score_button = Button(2, 'High score')
	click = False
	while True:

		mx, my = pygame.mouse.get_pos()

		screen.fill(bg_color)

		start_button.draw_on_screen()
		continue_button.draw_on_screen()
		high_score_button.draw_on_screen()

		if continue_button.rect.collidepoint((mx, my)):
			if click:
				game()

		if start_button.rect.collidepoint((mx, my)):
			if click:
				game_manager.reset_game()
				game()

		if high_score_button.rect.collidepoint((mx, my)):
			if click:
				high_score()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					click = True

		pygame.display.flip()
		clock.tick(30)

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

def high_score():
	with open("scores.json", "r") as read_file:
		scores = json.load(read_file)
	while True:
		screen.fill(bg_color)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pause_menu()
		
		text = font.render("High score", True, snake_color)
		text_rect = text.get_rect(center=(screen_width/2, 40))
		screen.blit(text, text_rect)

		for index, score in enumerate(scores["highScores"]):
			text = font.render(str(score), True, snake_color)
			text_rect = text.get_rect(center=(screen_width/2, 100 + 60*index))
			screen.blit(text, text_rect)
			if index > 5:
				break

		pygame.display.flip()
		clock.tick(30)

# General set_up
pygame.init()
clock = pygame.time.Clock()

# Game Display
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# some color and font
snake_color = (220, 220, 220)
food_color = (200, 0, 0)
bg_color = pygame.Color('Grey12')
font = pygame.font.Font('freesansbold.ttf', 24)

game_manager = GameManager()

# Enter the game memu
main_menu()