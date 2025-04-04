import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

Blue = (0, 0, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)
White = (255, 255, 255)

Screen_width = 400
Screen_height = 600
speed = 3
score = 0
coins = 0

font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 14)
game_over = font.render("Game Over", True, Black)

background = pygame.image.load("Images/AnimatedStreet.png")

screen = pygame.display.set_mode((Screen_width, Screen_height))
screen.fill(White)
pygame.display.set_caption("Racer")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < Screen_width and keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.top > 0 and keys[K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < Screen_height and keys[K_DOWN]:
            self.rect.move_ip(0, 5)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, Screen_width - 40), 0)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > 600:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, Screen_width - 40), 0)

c1 = c2 = c3 = c4 = c5 = False

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Images/coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, Screen_width - 40), random.randint(40, Screen_height - 40))
    
    def move(self):
        global coins, speed, c1, c2, c3, c4, c5
        if self.rect.bottom < Screen_height // 3:
            coins += 3
        elif self.rect.bottom < Screen_height // 1.5:
            coins += 2
        else:
            coins += 1

        if not c1 and coins >= 10:
            speed += 1
            c1 = True
        if not c2 and coins >= 20:
            speed += 1
            c2 = True
        if not c3 and coins >= 30:
            speed += 1
            c3 = True
        if not c4 and coins >= 40:
            speed += 1
            c4 = True
        if not c5 and coins >= 50:
            speed += 1
            c5 = True

        self.rect.center = (random.randint(40, Screen_width - 40), random.randint(40, Screen_height - 40))

# Спрайты
P = Player()
E = Enemy()
C = Coin()

enemies = pygame.sprite.Group()
enemies.add(E)
coinss = pygame.sprite.Group()
coinss.add(C)
all_sprites = pygame.sprite.Group()
all_sprites.add(P)
all_sprites.add(E)
all_sprites.add(C)

inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

def game_over_screen():
    screen.fill(Red)
    screen.blit(game_over, (130, 250))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                elif event.key == K_ESCAPE:
                    return False

background_y = 0

while True:
    for event in pygame.event.get():
        if event.type == inc_speed:
            speed += 0.1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    if pygame.sprite.spritecollideany(P, enemies):
        continue_game = game_over_screen()
        if not continue_game:
            pygame.quit()
            sys.exit()
        else:
            score = 0
            coins = 0
            speed = 3
            P.rect.center = (160, 520)
            E.rect.center = (random.randint(40, Screen_width - 40), 0)
            C.rect.center = (random.randint(40, Screen_width - 40), random.randint(40, Screen_height - 40))
            c1 = c2 = c3 = c4 = c5 = False

    background_y = (background_y + speed) % background.get_height()
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - background.get_height()))

    score_text = font_small.render("Score: " + str(score), True, Black)
    coin_text = font_small.render("Coins: " + str(coins), True, Black)
    screen.blit(score_text, (10, 10))
    screen.blit(coin_text, (310, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        if entity == C and pygame.sprite.spritecollideany(P, coinss):
            entity.move()
        elif entity != C:
            entity.move()

    for coin in coinss:
        coin.rect.y += speed
        if coin.rect.top > Screen_height:
            coin.rect.y = -coin.rect.height
            coin.rect.x = random.randint(40, Screen_width - 40)

    pygame.display.update()
    FramePerSec.tick(FPS)
