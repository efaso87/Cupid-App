import pygame
import sys
import random

# Initialize Pygame/game constants
pygame.init()
WIDTH, HEIGHT = 900, 700

# Adjust how fast pixels in game mive
FPS = 70

# Create/display color scheme for game
LIGHT_PINK = (255, 182, 193)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Love Catcher - Valentine's Day Mini Game")

# Insert timer for game
clock = pygame.time.Clock()

# Insert all images for gameplay:
# Cupid image
cupid_image = pygame.image.load("cupid.png")
cupid_width, cupid_height = 105, 105
cupid_image = pygame.transform.scale(cupid_image, (cupid_width, cupid_height))

# Heart image
heart_image = pygame.image.load("heart.gif")
heart_width, heart_height = 50, 50

# Play button image
play_button_image = pygame.image.load("playbutton.gif")
play_button_width, play_button_height = 275, 150
play_button_image = pygame.transform.scale(play_button_image, (play_button_width, play_button_height))
play_button_rect = play_button_image.get_rect()
play_button_rect.x = WIDTH // 2 - play_button_rect.width // 2
play_button_rect.y = HEIGHT // 2 - play_button_rect.height // 2

# Adjust cupid image measurements
cupid_rect = cupid_image.get_rect()
cupid_rect.x = WIDTH // 2 - cupid_rect.width // 2
cupid_rect.y = HEIGHT - 2 * cupid_rect.height

# List for heart positions
hearts = []

# Initialize game variables
score = 0
missed_hearts = 0
max_missed_hearts = 5
level = 1
hearts_per_level = 5
paused = False
playing = False

# Achievements
achievements = {
    "Catch 25 Hearts": False,
    "Catch 50 Hearts": False,
    "Reach Level 15": False,
}

# Function to reset game variables
def reset_game():
    global score, missed_hearts, level, hearts_per_level, hearts, playing
    score = 0
    missed_hearts = 0
    level = 1
    hearts_per_level = 5
    hearts = []
    playing = True

# Function to create a new heart
def create_heart():
    heart_rect = heart_image.get_rect()
    heart_rect.x = random.randint(0, WIDTH - heart_rect.width)
    heart_rect.y = 0
    hearts.append(heart_rect)

# Function to display achievements
def display_achievements():
    font = pygame.font.Font(None, 24)
    achievement_text = "Achievements:"
    screen.blit(font.render(achievement_text, True, RED), (10, HEIGHT - 80))

    i = 1
    for achievement, completed in achievements.items():
        status = "Achieved!" if completed else "Pending Achievement.."
        text = f"{i}. {achievement} - {status}"
        screen.blit(font.render(text, True, RED), (10, HEIGHT - 80 + i * 20))
        i += 1

# Main menu loop
while not playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):
                reset_game()

    # Draw main menu
    screen.fill(LIGHT_PINK)
    screen.blit(play_button_image, play_button_rect)
    display_achievements()
    pygame.display.flip()
    clock.tick(FPS)

# Game loop
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                # Toggle pause when 'P' key is pressed
                paused = not paused

    if not paused:
        # Move the character with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and cupid_rect.x > 0:
            cupid_rect.x -= 5
        if keys[pygame.K_RIGHT] and cupid_rect.x < WIDTH - cupid_rect.width:
            cupid_rect.x += 5

        # Move and create new hearts
        for heart_rect in hearts:
            heart_rect.y += 5
            if heart_rect.y > HEIGHT:
                hearts.remove(heart_rect)
                missed_hearts += 1
                if missed_hearts >= max_missed_hearts:
                    # Game over condition
                    print(f"Game Over! You finished with a score of {score}!")
                    playing = False

                # Achievement: Reach Level 15
                if level >= 15 and not achievements["Reach Level 15"]:
                    achievements["Reach Level 15"] = True
                    print("Achievement Unlocked: Reach Level 15!")

            # Check for collision between character and heart
            if cupid_rect.colliderect(heart_rect):
                hearts.remove(heart_rect)
                score += 1

                # Achievement: Catch 10 Hearts
                if score == 25 and not achievements["Catch 25 Hearts"]:
                    achievements["Catch 25 Hearts"] = True
                    print("Achievement Unlocked: Catch 25 Hearts!")

                # Achievement: Catch 20 Hearts
                if score == 50 and not achievements["Catch 50 Hearts"]:
                    achievements["Catch 50 Hearts"] = True
                    print("Achievement Unlocked: Catch 50 Hearts!")

        # Create new hearts if there are fewer than two on the screen
        if len(hearts) < 2 and random.randint(0, 100) < 5:  # Adjust the number to control heart creation frequency
            create_heart()

        # Level up condition
        if score % hearts_per_level == 0 and score > 0:
            level += 1
            hearts_per_level += 5
            print(f"Level up! You reached Level {level!s}")

    # Draw background, character, and hearts
    screen.fill(LIGHT_PINK)  # Set the background color to light pink
    screen.blit(cupid_image, cupid_rect)
    for heart_rect in hearts:
        screen.blit(pygame.transform.scale(heart_image, (heart_width, heart_height)), heart_rect)  # Adjust the size as needed

    # Display score and level
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, RED)
    level_text = font.render(f"Level: {level}", True, RED)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 50))

    # Pause message
    if paused:
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render("Paused", True, RED)
        screen.blit(pause_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

    # Display achievements
    display_achievements()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
