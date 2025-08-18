from flask import Flask
import random 

random_number = random.randint(0,9)
print(random_number)

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Guess a number between 0 and 9</h1>"\
            "<img scr='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnNoeWJsZjRhaGdrNWRwcWgwdDEyNGxoZTd6aWM1bTkzaTlyeHRnZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NfzERYyiWcXU4/giphy.gif'/>"

@app.route("/<int:guess>")
def guess_number(guess):
    if guess > random_number:
        return "<h1 style='color: purple'>Too high, try again!<h1>"\
                "<img src='https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnR2dmh3ODl0ZjFseGtvbmprYTV4anUzMWM0bGIxZzU0ZWE4OXZ2cCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MWSRkVoNaC30A/giphy.gif'/>"
    
    elif guess < random_number:
        return "<h1 style='color: red'>Too low, try again!</h1>"\
               "<img src='https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHpteGxjanRvajBwdjU0enY2cWh3dmZxemt6dGUyaGI1Z2w5dHBxcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/nR4L10XlJcSeQ/giphy.gif'/>"
        
    else:
        return "<h1 style='color: green'>You found me!</h1>" \
               "<img src='https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExcm44amVzOWt4NnducmtzOGY2dXFqZmwzYWRsYmplMGFlbnNjMDk0YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/MDJ9IbxxvDUQM/giphy.gif'/>"
    
if __name__ == "__main__":
    app.run(debug=True)     
