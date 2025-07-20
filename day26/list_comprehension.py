numbers = [1, 2, 3]
new_number  = [n + 1 for n in numbers]
# print(new_number)

name = "Sarvesh"
letter_list = [letter for letter in name]
# print(letter_list)


range_list = [num * 2 for num in range(1,5)]
# print(range_list)

# CONDITIONAL LIST COMPREHENSION
# new_list = [new_item for item in list if test]

names = ['sarvesh', 'jery', 'aman', 'sunny', 'arya']
short_names = [name for name in names if len(name) < 5]
# print(short_names)

long_names = [name.upper() for name in names if len(name) > 4]
# print(long_names)

numbers = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
squared_numbers = [num*num for num in numbers]
# print(squared_numbers)

list_of_strings = ['9', '0', '32', '8', '2', '8', '64', '29', '42', '99']
numbers = [int(num) for num in list_of_strings]
result = [n for n in numbers if n % 2 == 0]
# print(result)

# having file1.txt and file2.txt in day26 folder
with open(r"udemy\day26\file1.txt") as file1:
    file1_numbers = [int(line.strip()) for line in file1]
with open(r"udemy\day26\file2.txt") as file2:
    file2_numbers = [int(line.strip()) for line in file2]
result = [num for num in file1_numbers if num in file2_numbers]
print(result)

