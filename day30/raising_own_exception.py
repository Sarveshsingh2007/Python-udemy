height = float(input("Height:"))
Weight = int(input("Weight:"))

if height > 3:
    raise ValueError("Human Height should not be over 3 meters")

bmi = Weight / height ** 2  
print(bmi)
