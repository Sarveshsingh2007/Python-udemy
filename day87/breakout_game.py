import pygame
import random
import sys

pygame.init()

# Window settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Game settings
FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BRICK_WIDTH = 75
BRICK_HEIGHT = 25
ROWS = 6
COLS = 10

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 50, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [4, -4]

# Bricks
bricks = []
for row in range(ROWS):
    for col in range(COLS):
        brick_x = col * (BRICK_WIDTH + 5) + 35
        brick_y = row * (BRICK_HEIGHT + 5) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game Over flag
game_over = False

# Game Loop
clock = pygame.time.Clock()

while True:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 7
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 7

    if not game_over:
        # Move ball
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Wall collision
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        # Paddle collision
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # Brick collision
        hit_index = ball.collidelist(bricks)
        if hit_index != -1:
            brick = bricks.pop(hit_index)
            ball_speed[1] = -ball_speed[1]
            score += 10

        # Bottom collision - Game Over
        if ball.bottom >= HEIGHT:
            game_over = True

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, random.choice([RED, GREEN, YELLOW, BLUE]), brick)

    # Draw paddle and ball
    pygame.draw.rect(screen, BLUE, paddle)
    pygame.draw.circle(screen, WHITE, ball.center, BALL_RADIUS)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 10))

    # Check win
    if not bricks:
        win_text = font.render("🎉 YOU WIN! Press R to Restart", True, GREEN)
        screen.blit(win_text, (WIDTH // 2 - 200, HEIGHT // 2))
        game_over = True

    # Game over screen
    if game_over and bricks:
        over_text = font.render("💀 GAME OVER! Press R to Restart", True, RED)
        screen.blit(over_text, (WIDTH // 2 - 220, HEIGHT // 2))

    # Restart logic
    if game_over and keys[pygame.K_r]:
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_speed = [4, -4]
        paddle.x = WIDTH // 2 - PADDLE_WIDTH // 2
        bricks.clear()
        for row in range(ROWS):
            for col in range(COLS):
                brick_x = col * (BRICK_WIDTH + 5) + 35
                brick_y = row * (BRICK_HEIGHT + 5) + 50
                bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
        score = 0
        game_over = False

    # Update screen
    pygame.display.flip()
    clock.tick(FPS)
