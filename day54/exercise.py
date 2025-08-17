#Objective Create your own decorator function to measure the amount of seconds that a function takes to execute.

import time
current_time = time.time()
print(current_time) # seconds since Jan 1st, 1970 

# Write your code below 👇

def speed_calc_decorator(fuction):
  def wrapper():
    start_time = time.time
    function()
    end_time = time.time
    run_time = end_time-start_time
    print(f"{function.__name__} run speed: {run_time}s")

def fast_function():
  for i in range(1000000):
    i * i
        

def slow_function():
  for i in range(10000000):
    i * i

fast_function()
slow_function()    
