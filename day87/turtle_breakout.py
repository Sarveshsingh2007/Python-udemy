import turtle
import random
import time

# -------------------- Setup Window --------------------
win = turtle.Screen()
win.title("Breakout Game")
win.bgcolor("black")
win.setup(width=700, height=600)
win.tracer(0)

# -------------------- Paddle --------------------
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("blue")
paddle.shapesize(stretch_wid=1, stretch_len=6)
paddle.penup()
paddle.goto(0, -250)

# -------------------- Ball --------------------
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, -200)
ball.dx = 0.0   # ✅ start only after pressing key
ball.dy = 0.0

# -------------------- Score --------------------
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 260)
score_pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))

# -------------------- Restart Button --------------------
restart_btn = turtle.Turtle()
restart_btn.hideturtle()
restart_btn.penup()

# -------------------- Create Bricks --------------------
bricks = []
colors = ["red", "orange", "yellow", "green", "blue"]

def create_bricks():
    global bricks
    bricks.clear()
    for row in range(5):
        for col in range(10):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color(colors[row])
            brick.shapesize(stretch_wid=1, stretch_len=3)
            brick.penup()
            x = -315 + (col * 70)
            y = 250 - (row * 30)
            brick.goto(x, y)
            bricks.append(brick)

create_bricks()

# -------------------- Paddle Movement --------------------
def paddle_left():
    global game_started
    if not game_started:
        start_game()
    x = paddle.xcor()
    if x > -300:
        x -= 25
    paddle.setx(x)

def paddle_right():
    global game_started
    if not game_started:
        start_game()
    x = paddle.xcor()
    if x < 300:
        x += 25
    paddle.setx(x)

win.listen()
win.onkeypress(paddle_left, "Left")
win.onkeypress(paddle_right, "Right")

# -------------------- Start Game --------------------
game_started = False
game_over = False

def start_game():
    global game_started
    if not game_started:
        game_started = True
        ball.dx = 4.5   # ✅ Easy mode speed
        ball.dy = 4.5

# -------------------- Restart Game --------------------
def restart_game(x=None, y=None):
    global score, game_over, game_started
    score = 0
    score_pen.clear()
    score_pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))
    paddle.goto(0, -250)
    ball.goto(0, -200)
    ball.dx = 0
    ball.dy = 0
    create_bricks()
    game_started = False
    game_over = False
    restart_btn.clear()

# -------------------- Game Loop --------------------
while True:
    win.update()
    time.sleep(0.01)  # slight slowdown for smoothness

    if game_over:
        continue

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border check
    if ball.xcor() > 340:
        ball.setx(340)
        ball.dx *= -1

    if ball.xcor() < -340:
        ball.setx(-340)
        ball.dx *= -1

    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    if ball.ycor() < -290:
        score_pen.clear()
        score_pen.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
        game_over = True
        restart_btn.goto(0, -50)
        restart_btn.color("white")
        restart_btn.write("Click anywhere to Restart", align="center", font=("Courier", 20, "normal"))
        win.onscreenclick(restart_game)
        continue

    # Paddle collision
    if (ball.ycor() < -240 and ball.ycor() > -250) and (paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60):
        ball.sety(-240)
        ball.dy *= -1

    # Brick collision
    for brick in bricks[:]:
        if (ball.ycor() + 10 > brick.ycor() - 10 and
            ball.ycor() - 10 < brick.ycor() + 10 and
            ball.xcor() + 10 > brick.xcor() - 30 and
            ball.xcor() - 10 < brick.xcor() + 30):
            ball.dy *= -1
            brick.goto(1000, 1000)
            bricks.remove(brick)
            score += 10
            score_pen.clear()
            score_pen.write("Score: {}".format(score), align="center", font=("Courier", 24, "normal"))

    # Win condition
    if len(bricks) == 0:
        score_pen.clear()
        score_pen.write("YOU WIN!", align="center", font=("Courier", 36, "bold"))
        game_over = True
        restart_btn.goto(0, -50)
        restart_btn.color("white")
        restart_btn.write("Click anywhere to Restart", align="center", font=("Courier", 20, "normal"))
        win.onscreenclick(restart_game)

win.mainloop()
