#File not found
# with open("a_file.txt") as file:
#     file.read()

#Key error
# a_dictionary = {"key": "value"}
# value = a_dictionary("non_existing_key")

# Index error
# fruit_list = ["Apple"]
# fruit = fruit_list[3]

#type error
# text = "abc"
# print(text + 5)


# CATCHING EXCEPTION------------

# TRY - something that might cause an exception 
# EXCEPT - Do this if there was an exception
# Else - Do this if there were no exceptions
# FINALLY - Do this no matter what happens

try:
    file = open("a_file.txt")
    a_dictionary = {"key": "value"}
    print(a_dictionary["key"])

except FileNotFoundError:
    file = open(r"udemy\day30\a_file.txt", "w")
    file.write("Something")

except KeyError as error_message:
    print(f"That key {error_message} does not exist")

else:
    content = file.read()    
    print(content)

finally:
    file.close()
    print("File was closed")
