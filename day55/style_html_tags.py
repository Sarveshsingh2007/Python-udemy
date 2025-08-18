from flask import Flask

app = Flask(__name__)

# Decorators
def make_bold(function):
    def wrapper():
        return "<b>" + function() + "</b>"
    return wrapper

def make_emphasis(function):
    def wrapper():
        return "<em>" + function() + "</em>"
    return wrapper

def make_underlined(function):
    def wrapper():
        return "<u>" + function() + "</u
        
    return wrapper

# Using decorators
@app.route("/")
@make_bold
@make_emphasis
@make_underlined
def hello():
    return "Hello, Sarvesh!"

if __name__ == "__main__":
    app.run(debug=True)
