colours = {
    "apple": "red", 
    "pear": "green", 
    "banana": "yellow"
}

print(colours["apple"])

#append
colours["graphes"]= "green"
print(colours)

#creating empty dictionary
empty_dictionary = {}


# wipe an existing dictionary

# colours = {}
# print(colours)

#edit an item in an dictionary
colours["pear"] = "bitter"
print(colours)


# loop through a dictionary
for fruits in colours:
    print(fruits) # gives keys
    print(colours[fruits])   #  gives values 
