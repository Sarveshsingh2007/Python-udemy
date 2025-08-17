from flask import Flask
import random

app = Flask(__name__)

print(random.__name__)
print(__name__)

@app.route("/")
def hello_world():
    return "Hello, Flask"

@app.route("/bye")
def say_bye():
    return "Bye, Flask"

if __name__ == "__main__":
    app.run()
