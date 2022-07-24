import pygame
import random
import math
import time
from pygame import mixer

pygame.init()

# Game Window
wn = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Fight")
game_icon = pygame.image.load("ufo (3).png")
pygame.display.set_icon(game_icon)
background = pygame.image.load("background.png")

# Explosion
explosion = pygame.image.load("supernova.png")

# Audio
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 loops the background music

# InGame images(Player)
spaceship = pygame.image.load("spaceship.png")
playerx = 370
playery = 480
playerx_move = 0

# Enemy
alien = []
alienx = []
alieny = []
alienx_move = []
alieny_move = []
number_of_enemies = 6
for i in range(number_of_enemies):
    alien.append(pygame.image.load("ufo.png"))
    alienx.append(random.randint(50, 735))
    alieny.append(random.randint(50, 150))
    alienx_move.append(2)
    alieny_move.append(40)

# Score
score = 0
font = pygame.font.Font('04B_19.TTF', 32)
textx = 10
texty = 10

# Bullet
bullet = pygame.image.load("bullet.png")
bulletx = 0
bullety = 480
bullety_move = -4
state = "ready"

# Game Over text
game_over = pygame.font.Font('04B_19.TTF', 64)

# Game Start
restart = "stop"
begin = "stop"

# Starting Window
starting_text_font = pygame.font.Font('04B_19.TTF', 64)
space_to_start = pygame.font.Font('04B_19.TTF', 25)


def start_window():
    game_name = starting_text_font.render("SPACE FIGHT", True, (225, 225, 225))
    starting_text = space_to_start.render("PRESS SPACE TO START GAME", True, (225, 225, 225,))
    wn.blit(game_name, (225, 125))
    wn.blit(starting_text, (230, 350))


def explode(x, y):
    wn.blit(explosion, (x, y))


def game_over_text():
    over_text = game_over.render("GAME OVER", True, (255, 255, 255))  # Rendering game over Variable
    restart_text = font.render("PRESS ENTER TO RESTART", True, (255, 255, 255))
    wn.blit(over_text, (240, 250))
    wn.blit(restart_text, (225, 350))


def show_score(x, y):
    score_value = font.render("Score :" + str(score), True, (255, 255, 255))
    wn.blit(score_value, (x, y))


def is_collision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))

    # Collision distance check
    if distance < 27 and state == "fire":
        return True
    else:
        return False


def enemy(x, y, num):
    wn.blit(alien[num], (x, y))


def player(x, y):
    wn.blit(spaceship, (x, y))


def attack(x, y):
    wn.blit(bullet, (x, y))


# Information Screen
wn.fill((0, 0, 0))
info_name = starting_text_font.render("SPACE FIGHT", True, (225, 225, 225))
created_by = font.render("CREATED BY", True, (225, 225, 225))
creator = font.render("SANDIP", True, (225, 225, 225))
wn.blit(info_name, (225, 250))
wn.blit(created_by, (325, 350))
wn.blit(creator, (350, 400))
pygame.display.update()
time.sleep(1.25)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_move = -3.5
            if event.key == pygame.K_RIGHT:
                playerx_move = 3.5
            if event.key == pygame.K_UP:
                if state == "ready":

                    # Bullet Sound
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()

                    state = "fire"
                    bulletx = playerx + 16
            if event.key == pygame.K_RETURN:
                restart = "start"
                score = 0
            if event.key == pygame.K_SPACE:
                begin = "start"
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_move = 0

    # Window Customisation
    wn.fill((0, 0, 0))
    wn.blit(background, (0, 0))

    # Starting Window
    if begin == "stop":
        start_window()
        pygame.display.update()
        continue
    # Spaceship Movement
    playerx += playerx_move

    # Bullet Movement
    if state == "fire":
        bullety += bullety_move
        attack(bulletx, bullety)
    if bullety < 0:
        state = "ready"
        bullety = 480

    # Spaceship Boundary Check
    if playerx >= 740:
        playerx = 740
    if playerx <= 0:
        playerx = 0

    # Alien Movement
    for i in range(number_of_enemies):
        alienx[i] += alienx_move[i]

        # Restart
        if restart == "start":
            for k in range(number_of_enemies):
                alienx[k] = random.randint(50, 735)
                alieny[k] = random.randint(50, 150)
            restart = "stop"

        # Game Over
        if alieny[i] > 440:
            for j in range(number_of_enemies):
                alieny[j] = 2000
                game_over_text()
            restart = "stop"
            break

        # Alien Boundary Check
        if alienx[i] >= 740:
            alienx_move[i] = -1.5
            alieny[i] += alieny_move[i]
        if alienx[i] <= 0:
            alienx_move[i] = 1.5
            alieny[i] += alieny_move[i]

        # Collision
        if is_collision(alienx[i], alieny[i], bulletx, bullety):
            # Collision Sound
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()

            explode(alienx[i], alieny[i])
            bullety = 480
            state = "ready"
            alienx[i] = random.randint(50, 735)
            alieny[i] = random.randint(50, 150)
            score += 1
        enemy(alienx[i], alieny[i], i)

    player(playerx, playery)  # Player Movement
    show_score(textx, textx)
    pygame.display.update()  # Window Update
