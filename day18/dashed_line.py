from turtle import Turtle, Screen

tim = Turtle()

for _ in range(15):
    tim.pendown()
    tim.fd(10)
    tim.penup()
    tim.fd(10)

screen = Screen()
screen.exitonclick()
