import random
friends = ["Sarvesh", "Arpit", "Subhang", "Saurabh", "Sundram", "Ansh"]

# 1 Option
print(random.choice(friends))

# 2 Option

random_index = random.randint(0, 5)
print(friends[random_index])