import pygame
import os
import random
import math
import sys

WIDTH, HEIGHT = 1000, 1000  # Setting the width and height of the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Creating the game window
pygame.display.set_caption("Heart and Soul")    # Setting the window caption

WHITE = (255, 255, 255)     # Defining the color white

FPS = 60                    # Setting the frames per second for the game
VEL = 5                     # Setting the velocity of game objects
ENEMY_VEL = 3.5             # Setting the velocity of enemies

enemies = []                # Initializing an empty list for enemies

HEART_WIDTH = 70            # Setting the width of the heart character
HEART_HEIGHT = 60           # Setting the height of the heart character

SOUL_WIDTH = 350            # Setting the width of the soul character
SOUL_HEIGHT = 350           # Setting the height of the soul character

ENEMY_WIDTH = 100           # Setting the width of the enemy character
ENEMY_HEIGHT = 150          # Setting the height of the enemy character


# -----------------------------Characters --------------------
# Loading the image for the heart character
HEART_IMAGE = pygame.image.load(os.path.join('assets', 'heart.png'))
# Scaling the heart image to the desired size
HEART_IMAGE = pygame.transform.scale(HEART_IMAGE, (HEART_WIDTH, HEART_HEIGHT))

# Loading the image for the soul character
SOUL_IMAGE = pygame.image.load(os.path.join('assets', 'soul.png'))
# Scaling the soul image to the desired size
SOUL_IMAGE = pygame.transform.scale(SOUL_IMAGE, (SOUL_WIDTH, SOUL_HEIGHT))

# Loading and scaling images for different character variations
HEART_PIRATE = pygame.image.load(os.path.join('assets', 'heart_pirate.png'))
HEART_PIRATE = pygame.transform.scale(
    HEART_PIRATE, (HEART_WIDTH, HEART_HEIGHT))

SOUL_PIRATE = pygame.image.load(os.path.join('assets', 'soul_pirate.png'))
SOUL_PIRATE = pygame.transform.scale(SOUL_PIRATE, (SOUL_WIDTH, SOUL_HEIGHT))

HEART_NINJA = pygame.image.load(os.path.join('assets', 'heart_ninja.png'))
HEART_NINJA = pygame.transform.scale(HEART_NINJA, (HEART_WIDTH, HEART_HEIGHT))

SOUL_NINJA = pygame.image.load(os.path.join('assets', 'soul_ninja.png'))
SOUL_NINJA = pygame.transform.scale(SOUL_NINJA, (SOUL_WIDTH, SOUL_HEIGHT))

HEART_MUSICIAN = pygame.image.load(
    os.path.join('assets', 'heart_musician.png'))
HEART_MUSICIAN = pygame.transform.scale(
    HEART_MUSICIAN, (HEART_WIDTH, HEART_HEIGHT))

SOUL_MUSICIAN = pygame.image.load(os.path.join('assets', 'soul_musician.png'))
SOUL_MUSICIAN = pygame.transform.scale(
    SOUL_MUSICIAN, (SOUL_WIDTH, SOUL_HEIGHT))

ENEMY = pygame.image.load(os.path.join('assets', 'enemy.png'))
ENEMY = pygame.transform.scale(ENEMY, (ENEMY_WIDTH, ENEMY_HEIGHT))

# --------------------------------------------------------------

# -----------------------------Backgrounds--------------------
background_normal = pygame.image.load(
    os.path.join('assets', 'norma_background1.jpeg'))

background_pirate = pygame.image.load(
    os.path.join('assets', 'background_pirate.jpeg'))

background_ninja = pygame.image.load(
    os.path.join('assets', 'background_ninja.jpeg'))

background_musician = pygame.image.load(
    os.path.join('assets', 'background_musician.jpeg'))

# --------------------------------------------------------------

# -----------------------------Music--------------------
main_theme = "main_theme.mp3"

pygame.mixer.init()
pygame.mixer.music.load(f"music/{main_theme}")

# Set the volume (0.0 to 1.0)
volume = 0.2
pygame.mixer.music.set_volume(volume)

pygame.mixer.music.play(-1)  # -1 loops the song indefinitely


def spawn_enemy():
    # Creating a new enemy at a random position within the game window
    enemy = pygame.Rect(random.randint(0, WIDTH - ENEMY_WIDTH),
                        random.randint(0, HEIGHT - ENEMY_HEIGHT), ENEMY_WIDTH, ENEMY_HEIGHT)
    enemies.append(enemy)  # Adding the enemy to the list of enemies


def draw_window(soul, heart, enemies, score_text, background, h_image, s_image):
    # Drawing the background image on the window at position (0, 0)
    WIN.blit(background, (0, 0))

    # Drawing the soul image on the window at the current position (soul.x, soul.y)
    WIN.blit(s_image, (soul.x, soul.y))

    # Drawing each enemy in the enemies list on the window at their respective positions
    for enemy in enemies:
        WIN.blit(ENEMY, (enemy.x, enemy.y))

    # Drawing the heart image on the window at the current position (heart.x, heart.y)
    WIN.blit(h_image, (heart.x, heart.y))

    # Drawing the score text on the window at position (10, 10)
    WIN.blit(score_text, (10, 10))

    # Updating the display to show the changes
    pygame.display.update()


def heart_movement(keys_pressed, heart):
    # Moving the heart to the left if the 'A' key is pressed and the resulting position is within the window
    if keys_pressed[pygame.K_a] and heart.x - VEL > 0:
        heart.x -= VEL

    # Moving the heart to the right if the 'D' key is pressed and the resulting position is within the window
    if keys_pressed[pygame.K_d] and heart.x + VEL + heart.width < WIDTH:
        heart.x += VEL

    # Moving the heart up if the 'W' key is pressed and the resulting position is within the window
    if keys_pressed[pygame.K_w] and heart.y - VEL > 0:
        heart.y -= VEL

    # Moving the heart down if the 'S' key is pressed and the resulting position is within the window
    if keys_pressed[pygame.K_s] and heart.y + VEL + heart.height < HEIGHT:
        heart.y += VEL


def show_game_over_screen(score, level):
    font = pygame.font.Font(None, 80)

    if score == 0:
        # Game over screen for when the score is zero
        text = font.render("Game Over", True, (255, 0, 0))
        score_text = font.render(
            "Final Score: " + str(int(score)), True, (0, 0, 0))
        restart_text = font.render("Press ENTER to restart", True, (0, 0, 255))
        menu_text = font.render(
            "Press ESC to return to level select", True, (255, 0, 0))
    else:
        # Game over screen for when the score is not zero (heart and soul reunited)
        text = font.render("You reunited Heart and Soul!", True, (0, 255, 0))
        score_text = font.render("Score: " + str(int(score)), True, (0, 0, 0))
        restart_text = font.render(
            "Press ENTER to continue", True, (0, 0, 255))
        menu_text = font.render(
            "Press ESC to return to level select", True, (255, 0, 0))

    while True:
        WIN.fill(WHITE)

        # Positioning the text on the screen
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        restart_rect = restart_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 150))
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))

        # Blitting the text onto the screen
        WIN.blit(text, text_rect)
        WIN.blit(score_text, score_rect)
        WIN.blit(restart_text, restart_rect)
        WIN.blit(menu_text, menu_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Restarting the game with the specified level
                    start_game(level)
                elif event.key == pygame.K_ESCAPE:
                    show_menu_screen()  # Returning to the level select menu


def enemy_movement(heart, enemy):
    heart_center = heart.center
    enemy_center = enemy.center

    # Calculate the direction vector from the enemy to the heart
    direction_x = heart_center[0] - enemy_center[0]
    direction_y = heart_center[1] - enemy_center[1]

    # Normalize the direction vector
    direction_length = math.sqrt(direction_x ** 2 + direction_y ** 2)
    direction_x /= direction_length
    direction_y /= direction_length

    # Update the enemy position based on the normalized direction vector
    enemy.x += int(direction_x * ENEMY_VEL)
    enemy.y += int(direction_y * ENEMY_VEL)


def detect_collision(one, two, margin):
    # Add 0.5 to get the center pixel
    one_center = (one.center[0] + 0.5, one.center[1] + 0.5)
    two_center = (two.center[0] + 0.5, two.center[1] + 0.5)
    distance = math.dist(one_center, two_center)
    # Check if distance is less than 1.0 + margin
    return distance < (1.0 + margin)


def show_menu_screen():
    # setting up the font
    pygame.font.init()
    menu_font = pygame.font.Font(None, 80)
    menu_text = menu_font.render("Menu", True, (0, 0, 0))

    # defining the font for the level options
    level_font = pygame.font.Font(None, 60)
    level_text_1 = level_font.render("1 - Normal", True, (0, 0, 0))
    level_text_2 = level_font.render("2 - Pirate", True, (0, 0, 0))
    level_text_3 = level_font.render("3 - Ninja", True, (0, 0, 0))
    level_text_4 = level_font.render("4 - Musician", True, (0, 0, 0))
    exit_text = level_font.render("5 - Quit", True, (0, 0, 0))

    # defining the rectangles for the text

    WIN.fill(WHITE)
    menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 200))
    level_rect_1 = level_text_1.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 - 100))
    level_rect_2 = level_text_2.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    level_rect_3 = level_text_3.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 100))
    level_rect_4 = level_text_4.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 200))
    exit_rect = exit_text.get_rect(
        center=(WIDTH // 2, HEIGHT // 2 + 300))

    # blitting the rectangles and the text to the screen

    WIN.blit(menu_text, menu_rect)
    WIN.blit(level_text_1, level_rect_1)
    WIN.blit(level_text_2, level_rect_2)
    WIN.blit(level_text_3, level_rect_3)
    WIN.blit(level_text_4, level_rect_4)
    WIN.blit(exit_text, exit_rect)
    pygame.display.flip()

    # defining what to do when a specific key is presse
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    start_game("normal")
                elif event.key == pygame.K_2:
                    start_game("pirate")
                elif event.key == pygame.K_3:
                    start_game("ninja")
                elif event.key == pygame.K_4:
                    start_game("musician")
                elif event.key == pygame.K_5:
                    pygame.quit()


def start_game(level):
    global background, heart_image, soul_image

    # Set background and character images based on the selected level
    if level == "normal":
        background = background_normal
        heart_image = HEART_IMAGE
        soul_image = SOUL_IMAGE
    elif level == "pirate":
        background = background_pirate
        heart_image = HEART_PIRATE
        soul_image = SOUL_PIRATE
    elif level == "ninja":
        background = background_ninja
        heart_image = HEART_NINJA
        soul_image = SOUL_NINJA
    elif level == "musician":
        background = background_musician
        heart_image = HEART_MUSICIAN
        soul_image = SOUL_MUSICIAN

    # Initialize the positions of the soul and heart characters
    soul = pygame.Rect(random.randint(0, WIDTH - SOUL_WIDTH),
                       random.randint(0, HEIGHT - SOUL_HEIGHT), SOUL_WIDTH, SOUL_HEIGHT)
    heart = pygame.Rect(random.randint(0, WIDTH - HEART_WIDTH),
                        random.randint(0, HEIGHT - HEART_HEIGHT), HEART_WIDTH, HEART_HEIGHT)
    enemies.clear()

    # Ensure that the soul and heart are not too close to each other initially
    while abs(soul.x - heart.x) < 500 and abs(soul.y - heart.y) < 500:
        soul = pygame.Rect(random.randint(0, WIDTH - SOUL_WIDTH),
                           random.randint(0, HEIGHT - SOUL_HEIGHT), SOUL_WIDTH, SOUL_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    score = 0
    pygame.font.init()
    font = pygame.font.Font(None, 50)
    enemy_timer = 0
    spawn_enemy()

    while run:
        elapsed_time = clock.tick(FPS) / 1000
        enemy_timer += elapsed_time
        score += clock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        score_text = font.render(
            "Score: " + str(int(score)), True, (255, 255, 255))
        keys_pressed = pygame.key.get_pressed()

        # Spawn a new enemy every 3 seconds
        if enemy_timer >= 3:
            spawn_enemy()
            enemy_timer = 0

        for enemy in enemies:
            enemy_movement(heart, enemy)

            # Check for collision between enemy and heart
            if detect_collision(heart, enemy, 30):
                run = False
                score = 0

            # Check for collision between heart and soul
            if detect_collision(heart, soul, 70):
                run = False

        heart_movement(keys_pressed, heart)

        draw_window(soul, heart, enemies,
                    score_text, background, heart_image, soul_image)

    show_game_over_screen(score, level)


def main():
    show_menu_screen()


if __name__ == "__main__":
    main()
