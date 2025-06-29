print("Welcome to the tip calculator")
bill = float(input("What is the total bill? $"))
tip = int(input("How much tip would you like to give? 10, 12, or 15?"))
split = int(input("How many people to split the bill? "))

# total_bill = bill + (bill * tip / 100)
# amount_per_person = total_bill / split

# print(f"Each person should pay: ${round(amount_per_person, 2)}")

tip_as_percent = tip/100
total_tip_amount = bill * tip_as_percent
total_bill = bill + total_tip_amount
bill_per_person = total_bill / split
final_amount = round(bill_per_person, 2)
print(f"Each person should pay ${final_amount}")