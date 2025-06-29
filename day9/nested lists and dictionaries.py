capitals = {
    "India": "New Delhi",
    "Uttarakhand": "Dehradun"
}

# Nested list in dictionary
travel_log = {
    "India": ["uttarakhand", "punjab", "bihar"],
    "Uttarakhand": "Dehradun"
}
# print(travel_log)

# print(travel_log["India"][1])

# for country in travel_log:
#     print(travel_log[country])

nested_list = ["A", "b", ["C", "D"]]
# print(nested_list[2][1])

# nesting dictionary inside a dictionary

travel_log = {
    "Bihar": {
        "num_times_visited": 8,
        "total_visits": 12
    },
    "Hindustan": {
        "India": ["uttarakhand", "punjab", "bihar"],
        "Uttarakhand": ["Dehradun", "Mussorie"]
    },
}
print(travel_log["Hindustan"]["India"][2])