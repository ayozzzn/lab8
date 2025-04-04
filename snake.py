import pygame
import random
import sys

pygame.init()

width, height = 600, 400
cell_size = 20
FPS = 60            
speed = 10       
clock = pygame.time.Clock()

white = (255, 255, 255)
green = (0, 255, 0)
dark_green = (0, 155, 0)
red = (255, 0, 0)
black = (0, 0, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

font = pygame.font.SysFont("Verdana", 20)

snake = [(100, 100), (80, 100), (60, 100)]
direction = 'RIGHT'
score = 0
level = 1
move_counter = FPS // speed 

walls = []
for x in range(0, width, cell_size):
    walls.append((x, 0))
    walls.append((x, height - cell_size))
for y in range(0, height, cell_size):
    walls.append((0, y))
    walls.append((width - cell_size, y))

def generate_food():
    while True:
        x = random.randint(1, (width // cell_size) - 2) * cell_size
        y = random.randint(1, (height // cell_size) - 2) * cell_size
        if (x, y) not in snake and (x, y) not in walls:
            return (x, y)

food = generate_food()

def draw():
    screen.fill(white)

    for wall in walls:
        pygame.draw.rect(screen, black, (wall[0], wall[1], cell_size, cell_size))

    for part in snake:
        pygame.draw.rect(screen, green, (part[0], part[1], cell_size, cell_size))

    pygame.draw.rect(screen, red, (food[0], food[1], cell_size, cell_size))

    score_text = font.render(f"Score: {score}  Level: {level}", True, dark_green)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

running = True
while running:
    clock.tick(FPS)
    move_counter += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    if move_counter >= FPS // speed:
        move_counter = 0

        head_x, head_y = snake[0]
        if direction == 'UP':
            head_y -= cell_size
        elif direction == 'DOWN':
            head_y += cell_size
        elif direction == 'LEFT':
            head_x -= cell_size
        elif direction == 'RIGHT':
            head_x += cell_size

        new_head = (head_x, head_y)

        if new_head in walls or new_head in snake or head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
            print("Game Over")
            running = False
            break

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = generate_food()
            if score % 3 == 0:
                level += 1
                speed += 2
        else:
            snake.pop()

        draw()  
