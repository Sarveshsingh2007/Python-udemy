############ QUESTION 1 #############

def a_function(a_parameter):
    a_variable = 15
    return a_parameter
 
a_function(10)
# print(a_variable) ERROR ------- NameError

############ QUESTION 2 #############

i = 50
def foo():
    i = 100
    return i
 
foo()
# print(i)

############ QUESTION 3 #############

def bar():
    my_variable = 9
 
    if 16 > 9:
      my_variable = 16
 
    print(my_variable)
 
bar()
