import turtle as t   
import random

tim = t.Turtle()

colors = ["cyan", "medium spring green", "red","blue", "orange", "purple", "yellow", "magenta", "lime green", "deep pink"]
directions = [0, 90, 180, 270]
tim.pensize(10)
tim.speed("fastest")

for _ in range(200):
    tim.color(random.choice(colors))
    tim.forward(30)
    tim.setheading(random.choice(directions))