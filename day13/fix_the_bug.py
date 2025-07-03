# age = int(input("How old are you?"))

# if we will input 15 as string(fifteen) it will show error ValueError
# for solve that problem we will use try and except block

# if age > 18:
# print("You can drive at age {age}.") not showing the age in the print statement because age is int type and it is not a string



try:
    age = int(input("How old are you? "))

except ValueError:
    print("You have typed in a an invalid number. please try again with a numerical response such as 15\n")  
    age = int(input("How old are you? "))

if age > 18:
    print(f"You can drive at age {age}.")
