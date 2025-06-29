import random
import my_module # imported own module 

random_number = random.randint(1, 10)
# print(random_number)
# print(my_module.my_favourite_number) 

# random.random() # returns floating point numbers
random_number_0_to_1 = random.random() * 10
# print(random_number_0_to_1) #prints floating point number only 0 and don't include 1 

# print(round(random_number_0_to_1, 2)) # prints 2 digts after point used round(function, digits to print after point)

# random.uniform(a, b) returns random floating number between a and b
random_float = random.uniform(1, 20)
# print(random_float)


#--------HEADS AND TAILS--------#

Heads_or_Tails = random.randint(0, 1)
if Heads_or_Tails == 0:
    print("Heads")
else:
    print("Tails")    