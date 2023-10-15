import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
FRUIT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue
BASKET_COLOR = (50, 50, 50)
FONT = pygame.font.Font(None, 36)

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Catcher")

# Basket settings
basket_width, basket_height = 100, 20
basket_x = (WIDTH - basket_width) // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 10

# Fruit settings
fruit_width, fruit_height = 40, 40
fruit_speed = 5
fruits = []

# Score
score = 0

# Game over flag
game_over = False

# New variables
initial_fruit_spawn_rate = 0.01  # Initial rate of fruit spawn
max_fruit_spawn_rate = 0.2  # Maximum rate of fruit spawn
missed_fruits = 0  # Number of fruits missed
high_score = 0  # Initialize high score (you can load it from a file if needed)

# Functions
def draw_basket(x, y):
    pygame.draw.rect(screen, BASKET_COLOR, (x, y, basket_width, basket_height))

def draw_fruit(x, y, color):
    pygame.draw.ellipse(screen, color, (x, y, fruit_width, fruit_height))

def display_score(score):
    score_text = FONT.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

def game_over_screen():
    game_over_text = FONT.render("Game Over", True, WHITE)
    score_text = FONT.render("Your Score: " + str(score), True, WHITE)
    high_score_text = FONT.render("High Score: " + str(high_score), True, WHITE)
    restart_text = FONT.render("Press R to Restart", True, WHITE)

    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    screen.blit(high_score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 50))
    screen.blit(restart_text, (WIDTH // 2 - 120, HEIGHT // 2 + 100))

# ...
# ... (previous code)

# New variable to track the final statistics display state
show_final_stats = False

# Game loop
clock = pygame.time.Clock()
fruit_spawn_rate = initial_fruit_spawn_rate  # Initialize fruit spawn rate

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Restart the game
                score = 0
                fruits = []
                game_over = False
                missed_fruits = 0  # Reset missed fruits
                fruit_spawn_rate = initial_fruit_spawn_rate  # Reset fruit spawn rate
                show_final_stats = False  # Reset the flag

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    if not game_over:
        # Adjust fruit spawn rate
        if fruit_spawn_rate < max_fruit_spawn_rate:
            fruit_spawn_rate += 0.0001  # Increase the spawn rate over time

        # Generate new fruits based on spawn rate
        if random.random() < fruit_spawn_rate:
            fruit_x = random.randint(0, WIDTH - fruit_width)
            fruit_color = random.choice(FRUIT_COLORS)
            fruits.append([fruit_x, 0, fruit_color])

        # Move fruits
        for fruit in fruits:
            fruit[1] += fruit_speed

        # Check for collisions
        for fruit in fruits:
            if (
                basket_x < fruit[0] + fruit_width
                and basket_x + basket_width > fruit[0]
                and basket_y < fruit[1] + fruit_height
                and basket_y + basket_height > fruit[1]
            ):
                if fruit[2] != (0, 0, 255):  # Check if the fruit is not blue (rotten)
                    score += 1
                fruits.remove(fruit)

        # Remove fruits that go out of the screen
        fruits = [fruit for fruit in fruits if fruit[1] < HEIGHT]

        # Game over condition
        for fruit in fruits:
            if fruit[1] >= HEIGHT:
                missed_fruits += 1  # Increment missed fruit count
                fruits.remove(fruit)

        # Check if the player has missed 10 fruits
        if missed_fruits >= 10:
            game_over = True
            show_final_stats = True  # Set the flag to display final statistics

        # Update high score
        if score > high_score:
            high_score = score

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw the basket
        draw_basket(basket_x, basket_y)

        # Draw the fruits
        for fruit in fruits:
            draw_fruit(fruit[0], fruit[1], fruit[2])

        # Display the score
        display_score(score)

    pygame.display.flip()
    clock.tick(FPS)

    # Display final statistics and wait for key press
    if show_final_stats:
        game_over_screen()
        final_stats_text = FONT.render(
            f"Total Fruits Caught: {score}   High Score: {high_score}",
            True,
            WHITE
        )
        screen.blit(final_stats_text, (WIDTH // 2 - 220, HEIGHT // 2 + 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
