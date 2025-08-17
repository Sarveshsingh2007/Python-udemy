import time

def delay_decorator(function):
    def wrapper_function():
        time.sleep(2)
        # do something before function
        function()
        function()
        # do something after function
    return wrapper_function    

@delay_decorator
def say_hello():
    print("Hello Sarvesh")

@delay_decorator
def say_bye():
    print("Bye Sarvesh")

def say_greeting():
    print("How are you buddy?")

say_hello()  

decorated_function = delay_decorator(say_greeting)
decorated_function()
