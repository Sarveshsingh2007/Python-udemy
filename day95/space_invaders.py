"""
Space Invaders - Turtle implementation
Controls:
  - Left Arrow / Right Arrow: move ship
  - Space: fire bullet

Save as space_invaders_turtle.py and run with: python space_invaders_turtle.py

Made to be readable and easy to modify for assignment purposes.
"""
import turtle
import random
import time

# ---------- Config ----------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SPEED = 20
BULLET_SPEED = 20
ENEMY_X_SPACING = 60
ENEMY_Y_SPACING = 50
ENEMY_SPEED_X = 10
ENEMY_DROP = 30
ENEMY_MOVE_INTERVAL_MS = 600  # move enemies every N milliseconds
NUM_ENEMY_ROWS = 4
NUM_ENEMY_COLS = 8
BARRIER_COUNT = 4
BARRIER_WIDTH = 70
BARRIER_HEIGHT = 30
BARRIER_HEALTH = 3

# ---------- Setup screen ----------
screen = turtle.Screen()
screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
screen.title("Space Invaders - Turtle Edition")
screen.bgcolor("black")
screen.tracer(0)

# ---------- Utility helpers ----------

def create_turtle(shape="square", color="white", stretch_w=1, stretch_h=1):
    t = turtle.Turtle()
    t.hideturtle()
    t.shape(shape)
    t.color(color)
    t.penup()
    t.speed(0)
    try:
        t.shapesize(stretch_h, stretch_w)
    except Exception:
        pass
    t.showturtle()
    return t


def is_collision(a, b, threshold=20):
    return a.distance(b) < threshold

# ---------- Player ----------
player = create_turtle("triangle", "white", 1.5, 1.5)
player.setheading(90)
player.goto(0, -SCREEN_HEIGHT//2 + 60)

# ---------- Scoreboard / HUD ----------
score = 0
lives = 3

hud = create_turtle("square", "black")
hud.hideturtle()


def update_hud():
    hud.clear()
    hud.goto(-SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2 - 40)
    hud.color("white")
    hud.write(f"Score: {score}", font=("Arial", 14, "normal"))
    hud.goto(SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 - 40)
    hud.write(f"Lives: {lives}", font=("Arial", 14, "normal"))

# ---------- Bullet (single) ----------
bullet = create_turtle("square", "yellow", 0.4, 0.8)
bullet.hideturtle()
bullet_state = "ready"  # "ready" or "fire"


def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x, y = player.position()
        bullet.goto(x, y + 20)
        bullet.showturtle()

# ---------- Barriers ----------
barriers = []

class Barrier:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = BARRIER_HEALTH
        self.t = create_turtle("square", "green", BARRIER_WIDTH/20, BARRIER_HEIGHT/20)
        self.t.goto(x, y)

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.destroy()
        else:
            # darken color
            if self.health == 2:
                self.t.color("yellow")
            else:
                self.t.color("orange")

    def destroy(self):
        self.t.hideturtle()
        try:
            barriers.remove(self)
        except ValueError:
            pass

# create barrier positions
barrier_start_x = -SCREEN_WIDTH//4
for i in range(BARRIER_COUNT):
    bx = barrier_start_x + i * (SCREEN_WIDTH//(BARRIER_COUNT))
    by = -SCREEN_HEIGHT//2 + 140
    barriers.append(Barrier(bx, by))

# ---------- Enemies ----------
enemies = []
enemy_direction = 1  # 1: moving right, -1: moving left

def create_enemy(x, y):
    e = create_turtle("square", "red", 1.5, 1)
    e.goto(x, y)
    enemies.append(e)

# populate grid
start_x = -(NUM_ENEMY_COLS-1) * ENEMY_X_SPACING / 2
start_y = SCREEN_HEIGHT//2 - 120
for row in range(NUM_ENEMY_ROWS):
    for col in range(NUM_ENEMY_COLS):
        x = start_x + col * ENEMY_X_SPACING
        y = start_y - row * ENEMY_Y_SPACING
        create_enemy(x, y)

# ---------- Movement and input handlers ----------

def move_left():
    x, y = player.position()
    x -= PLAYER_SPEED
    left_bound = -SCREEN_WIDTH//2 + 20
    if x < left_bound:
        x = left_bound
    player.setx(x)


def move_right():
    x, y = player.position()
    x += PLAYER_SPEED
    right_bound = SCREEN_WIDTH//2 - 20
    if x > right_bound:
        x = right_bound
    player.setx(x)

screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# ---------- Enemy movement tick ----------

def enemies_move_tick():
    global enemy_direction, ENEMY_SPEED_X, ENEMY_MOVE_INTERVAL_MS, lives
    # compute if any enemy is at edge
    shift_down = False
    for e in enemies:
        if not e.isvisible():
            continue
        new_x = e.xcor() + enemy_direction * ENEMY_SPEED_X
        if new_x > SCREEN_WIDTH//2 - 30 or new_x < -SCREEN_WIDTH//2 + 30:
            shift_down = True
            break
    if shift_down:
        enemy_direction *= -1
        for e in enemies:
            if e.isvisible():
                e.sety(e.ycor() - ENEMY_DROP)
                # check if any enemy hit player zone
                if e.ycor() <= player.ycor() + 20:
                    game_over()
                    return
    else:
        for e in enemies:
            if e.isvisible():
                e.setx(e.xcor() + enemy_direction * ENEMY_SPEED_X)
    # schedule next move
    screen.ontimer(enemies_move_tick, ENEMY_MOVE_INTERVAL_MS)

# ---------- Collision and game loop ----------

def game_over(win=False):
    global running
    running = False
    hud.goto(0, 20)
    hud.color("white")
    if win:
        hud.write("YOU WIN! Press Esc to exit.", align="center", font=("Arial", 24, "bold"))
    else:
        hud.write("GAME OVER - Press Esc to exit.", align="center", font=("Arial", 24, "bold"))


def check_collisions():
    global bullet_state, score, lives
    # bullet vs enemies
    if bullet_state == "fire":
        for e in enemies:
            if e.isvisible() and is_collision(bullet, e, threshold=25):
                # hit
                e.hideturtle()
                try:
                    enemies.remove(e)
                except ValueError:
                    pass
                bullet.hideturtle()
                bullet_state = "ready"
                score += 10
                update_hud()
                break
        # bullet vs barriers
        for b in list(barriers):
            if bullet_state == "fire" and is_collision(b.t, bullet, threshold=30):
                b.hit()
                bullet.hideturtle()
                bullet_state = "ready"
                break

    # enemies vs player (collision)
    for e in enemies:
        if e.isvisible() and is_collision(e, player, threshold=25):
            # player loses
            lose_life()
            break

    # enemies reach bottom
    for e in enemies:
        if e.isvisible() and e.ycor() <= player.ycor() + 10:
            game_over()
            return

    # enemies win check: none left
    if len(enemies) == 0:
        game_over(win=True)


def lose_life():
    global lives, running
    lives -= 1
    update_hud()
    # flash player
    player.hideturtle()
    screen.update()
    time.sleep(0.5)
    player.showturtle()
    if lives <= 0:
        game_over()

# ---------- Main game loop ----------

running = True
update_hud()
# start enemy movement
screen.ontimer(enemies_move_tick, ENEMY_MOVE_INTERVAL_MS)

# main update loop

def main_loop():
    global bullet_state
    if not running:
        return
    # move bullet if fired
    if bullet_state == "fire":
        bullet.sety(bullet.ycor() + BULLET_SPEED)
        # if bullet off screen
        if bullet.ycor() > SCREEN_HEIGHT//2:
            bullet.hideturtle()
            bullet_state = "ready"
    # enemies occasionally shoot (optional, simple version)
    # check collisions
    check_collisions()
    screen.update()
    # call repeatedly
    screen.ontimer(main_loop, 20)

# exit key

def exit_game():
    screen.bye()

screen.onkey(exit_game, "Escape")

# start main loop
main_loop()

# keep window open
screen.mainloop()
