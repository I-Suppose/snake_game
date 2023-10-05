import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kawaii Snake Game :3")

def reset_game():
    global snake, snake_direction, snake_growth, food, score
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (0, -1)
    snake_growth = False
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0

reset_game()  # Initialize the game

# Game Loop
running = True
clock = pygame.time.Clock()

# Create a font for the score
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != (0, 1):
                snake_direction = (0, -1)
            elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                snake_direction = (0, 1)
            elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                snake_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                snake_direction = (1, 0)

    # Update Snake
    head_x, head_y = snake[0]
    new_head = (head_x + snake_direction[0], head_y + snake_direction[1])

    if new_head == food:
        snake_growth = True
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        score += 1  # Increase the score when the snake eats a fruit

    snake.insert(0, new_head)

    if not snake_growth:
        snake.pop()
    snake_growth = False

    # Check for Game Over
    if (
        new_head[0] < 0
        or new_head[0] >= GRID_WIDTH
        or new_head[1] < 0
        or new_head[1] >= GRID_HEIGHT
        or new_head in snake[1:]
    ):
        # Game Over Screen
        game_over_text = font.render("Game Over! Press 'R' to Restart", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()

        # Wait for 'R' key to be pressed to restart
        restart = False
        while not restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    restart = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        reset_game()
                        restart = True

    # Draw everything
    screen.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(
            screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

    pygame.draw.rect(
        screen, WHITE, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    )

    # Draw the score at the top right corner
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
    screen.blit(score_text, score_rect)

    pygame.display.flip()

    clock.tick(10)

pygame.quit()
