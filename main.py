import pygame
import random
import time
import os


pygame.init()

pygame.font.init()

WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


PLAYER_VEL = 10

FONT = pygame.font.SysFont("calibri", 44)

ALIEN_WIDTH = 40
ALIEN_HEIGHT = 40
ALIEN_VEL = 5

COLLISION_SOUND = pygame.mixer.Sound(os.path.join("assets", "collision.wav"))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("assets", "game_over.wav"))
GAME_PLAY_SOUND = pygame.mixer.Sound(os.path.join("assets", "bg_music.wav"))

GAME_PLAY_SOUND.play(-1)

pygame.display.set_caption("SPAZE-EVADER")
clock = pygame.time.Clock()


BG = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "bg.jpg")), (1400, 800)
)


def draw(player, player_rect, elapsed_time, aliens, life_remaining):
    WIN.blit(BG, (0, 0))

    WIN.blit(player, player_rect)

    for alien, alien_rect in aliens:
        WIN.blit(alien, alien_rect)

    time_text = FONT.render(f"Time: {int(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (4, 4))

    n = 1
    for _ in range(life_remaining):
        heart = pygame.transform.scale(
            pygame.image.load(os.path.join("assets", "heart.png")), (30, 30)
        )
        WIN.blit(heart, (WIDTH - n * (30 + 10), 20))
        n += 1

    pygame.display.update()


def main():
    player = pygame.transform.scale(
        pygame.image.load(os.path.join("assets", "spaceship.png")).convert_alpha(),
        (75, 75),
    )

    player_rect = player.get_rect(midbottom=(WIDTH // 2, HEIGHT))
    life_remaining = 5

    start_time = time.time()
    elapsed_time = 0

    # Regarding aliens

    alien_add_increment = 2000
    alien_count = 0

    aliens = []

    hit = False

    # MAIN GAME LOOP #

    while True:
        alien_count += clock.tick(80)
        if alien_count > alien_add_increment:
            for _ in range(5):
                alien_x = random.randint(0, WIDTH - ALIEN_WIDTH)
                alien = pygame.transform.scale(
                    pygame.image.load(os.path.join("assets", "alien.png")),
                    (
                        ALIEN_WIDTH,
                        ALIEN_HEIGHT,
                    ),
                )

                alien_rect = alien.get_rect(topleft=(alien_x, -ALIEN_HEIGHT))

                aliens.append((alien, alien_rect))

            alien_count = 0
            alien_add_increment = max(600, alien_add_increment - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        key_pressed = pygame.key.get_pressed()

        elapsed_time = time.time() - start_time

        if (key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]) and (
            player_rect.x + PLAYER_VEL + player_rect.width
        ) <= WIDTH:
            player_rect.x += PLAYER_VEL
        if (
            key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]
        ) and player_rect.x - PLAYER_VEL >= 0:
            player_rect.x -= PLAYER_VEL

        # ALIEN GENERATION AND COLLISION #

        for alien, alien_rect in aliens:
            alien_rect.y += ALIEN_VEL

            if alien_rect.y > HEIGHT:
                aliens.remove((alien, alien_rect))
            elif alien_rect.colliderect(player_rect):
                aliens.remove((alien, alien_rect))
                hit = True
                break

        if hit:
            life_remaining -= 1
            COLLISION_SOUND.play()
            hit = False

        if life_remaining == 0:
            lost_text = FONT.render("You were hit! Game Over!", True, "#ffafaf")
            WIN.blit(lost_text, (WIDTH // 2 - lost_text.get_width() // 2, HEIGHT // 2))
            pygame.display.update()
            GAME_OVER_SOUND.play()
            pygame.time.delay(5000)
            break

        draw(player, player_rect, elapsed_time, aliens, life_remaining)

        clock.tick(80)


if __name__ == "__main__":
    main()
