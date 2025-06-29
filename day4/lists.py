states_of_india = ["Uttarakhand", "Bihar", "Punjab", "Kashmir", "Haryana"]

# print(states_of_india[-1])
# print(states_of_india[1])

states_of_india[-1] = "Mumbai"
# print(states_of_india[-1])


#append
states_of_india.append("Rajsthan")
# print(states_of_india)

#extend
states_of_india.extend(["Uttar Pradesh", "Assam"])
# print(states_of_india)

#insert
states_of_india.insert(2, "Madhya Pradesh")
# print(states_of_india)

states_of_india.remove("Assam")
# print(states_of_india)

states_of_india.pop()
print(states_of_india)
