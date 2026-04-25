import pygame
import time
import random
import os

pygame.init()
pygame.font.init()

BASE_DIR = os.path.dirname(__file__) 

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Bullet")

try:
    bg_path = os.path.join(BASE_DIR, "bg.jpeg")
    BG = pygame.image.load(bg_path).convert()
    BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
except:
    print("Background missing → using fallback")
    BG = pygame.Surface((WIDTH, HEIGHT))
    BG.fill((20, 20, 20))


PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", True, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "blue", player)

    for star in stars:
        pygame.draw.rect(WIN, "red", star)

    pygame.display.update()


def main():
    run = True

    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()
    start_time = time.time()

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

    
        for star in stars[:]:
            star.y += STAR_VEL

            if star.y > HEIGHT:
                stars.remove(star)

            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        
        if hit:
            WIN.blit(BG, (0, 0))
            lost_text = FONT.render("YOU LOST!", True, "white")
            WIN.blit(lost_text, (
                WIDTH/2 - lost_text.get_width()/2,
                HEIGHT/2 - lost_text.get_height()/2
            ))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False
            continue

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main()
