# len(12345) #TypeError

len("Hello")

# Typechecking
# print(type("Hello"))
# print(type(234))
# print(type(234.34))
# print(type(True))

# # Type-Conversion/ Type-casting
# print(int("123") + int("456")) #converted string to integer output is 579
# print("123" + "456") #output 123456

# print(int("abc") + int("456")) #ValueError
 
name_of_the_user = input("Enter your name: ") # str
length_of_name = len(name_of_the_user) # int

print(type("Number of letters in your name: "))
print(type(length_of_name))

print("Number of letters in your name: " + str(length_of_name))
