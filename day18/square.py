from turtle import Turtle, Screen

tim = Turtle()

for _ in range(4):
    tim.fd(100)
    tim.right(90)


screen = Screen()
screen.exitonclick()
