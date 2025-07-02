# enemies = 1

# def increase_enemies():
#     enemies = 2
#     print(f"enemies inside function: {enemies}")

# increase_enemies()
# print(f"enemies outside function: {enemies}")    
print("GLOBAL VARIBLE: A variable declared outside all the functions, accessible throughout the program.\n\n")
print("LOCAL VARIBLE: A variable declared inside a function, only accessible within that function.\n\n ")
print("Namespace: It is a container that holds names like variables and functions")
print("\n"*5)


# Local scope 
print("LOCAL SCOPE ")


def drink_potion():
    potion_strength = 2
    print(potion_strength)

drink_potion()
# print(potion_strength)    potion_strength is not defined (NameError)



# Global scope
print("\n\n\n\nGLOBAL SCOPE ")


palyer_health = 10 # global variable 

def game():
    def drink_potion():
        potion_strength = 2 # local variable 
        print(palyer_health)
        
drink_potion()   
print(palyer_health) 
