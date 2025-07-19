import turtle
import pandas

screen = turtle.Screen()
screen.title("India States Game")
image = r"udemy\day25\India_states_game\india_map.gif"
screen.addshape(image)
turtle.shape(image)

screen.setup(642, 772)

data = pandas.read_csv(r"udemy\day25\India_states_game\india_states.csv")
all_states = data.state.to_list()
guessed_states = []

while len(guessed_states) < 30:
    answer_state = screen.textinput(title=f"{len(guessed_states)}/30 States Correct",
                                     prompt="What's another state's name?").title()

    if answer_state == "Exit":
        missing_states = []
        for state in all_states:
            if state not in guessed_states:
                missing_states.append(state)
        new_data = pandas.DataFrame(missing_states)   
        new_data.to_csv(r"udemy\day25\India_states_game\states_to_learn.csv")     
        break
    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data.state == answer_state]
        t.goto(state_data.x.item(), state_data.y.item())
        t.write(answer_state)


screen.exitonclick()    
