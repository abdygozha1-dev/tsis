import pygame
import random
import sys

pygame.init()

SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("TSIS 3 Racer Game")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,215,0)
CYAN = (0,200,255)

car = pygame.Rect(400, 500, 40, 80)

state = "menu"

speed = 5
score = 0
distance = 0

enemies = []
coins = []
powerups = []

active_power = None
power_timer = 0

def reset_game():
    global car, speed, score, distance, enemies, coins, powerups, active_power, power_timer
    car.x, car.y = 400, 500
    speed = 5
    score = 0
    distance = 0
    enemies = []
    coins = []
    powerups = []
    active_power = None
    power_timer = 0

def spawn_enemy():
    if random.randint(1, 40) == 1:
        x = random.choice([300, 400, 500])
        enemies.append(pygame.Rect(x, 0, 40, 80))

def spawn_coin():
    if random.randint(1, 60) == 1:
        x = random.choice([300, 400, 500])
        coins.append(pygame.Rect(x, 0, 20, 20))

def spawn_power():
    if random.randint(1, 200) == 1:
        x = random.choice([300, 400, 500])
        powerups.append(pygame.Rect(x, 0, 30, 30))

def move_objects():
    for e in enemies:
        e.y += speed
    for c in coins:
        c.y += speed
    for p in powerups:
        p.y += speed

def check_collisions():
    global score, active_power, power_timer, speed, state

    for e in enemies[:]:
        if car.colliderect(e):
            if active_power == "shield":
                enemies.remove(e)
                active_power = None
            else:
                state = "gameover"

    for c in coins[:]:
        if car.colliderect(c):
            score += 1
            coins.remove(c)

    for p in powerups[:]:
        if car.colliderect(p):
            active_power = random.choice(["nitro", "shield", "repair"])
            power_timer = 300
            powerups.remove(p)

def update_power():
    global active_power, power_timer, speed

    if active_power:
        power_timer -= 1
        if active_power == "nitro":
            speed = 10
        else:
            speed = 5
        if power_timer <= 0:
            active_power = None

running = True

while running:
    screen.fill((20,20,20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game()
                state = "game"

        elif state == "gameover":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    state = "game"
                if event.key == pygame.K_m:
                    state = "menu"

    if state == "menu":
        text = font.render("PRESS ENTER TO PLAY", True, WHITE)
        screen.blit(text, (220, 300))

    elif state == "game":
        distance += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            car.x -= 5
        if keys[pygame.K_RIGHT]:
            car.x += 5

        spawn_enemy()
        spawn_coin()
        spawn_power()

        move_objects()
        check_collisions()
        update_power()

        pygame.draw.rect(screen, RED, car)

        for e in enemies:
            pygame.draw.rect(screen, GREEN, e)

        for c in coins:
            pygame.draw.rect(screen, YELLOW, c)

        for p in powerups:
            pygame.draw.rect(screen, CYAN, p)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Distance: {distance}", True, WHITE), (10, 40))

        if active_power:
            screen.blit(font.render(f"Power: {active_power}", True, WHITE), (10, 70))

    elif state == "gameover":
        screen.blit(font.render("GAME OVER", True, RED), (300, 250))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (300, 300))
        screen.blit(font.render("R - Retry | M - Menu", True, WHITE), (220, 350))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()