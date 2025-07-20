# new_dict = {new_key: new_value for item in list}

# new_dict = {new_key: new_value for (key,value) in dict.items()}

# new_dict = {new_key: new_value for (key,value) in dict.items() if test}

# students_score = {
#     "sarvesh": 90,
#     "jery": 80,
#     "aman": 70,
#     "sunny": 60,
#     "arya": 50
# }
import random

names = names = ['sarvesh', 'jery', 'aman', 'sunny', 'arya']
students_scores = {student:random.randint(50, 100) for student in names}
# print(students_scores)

# passed_students = {
#     "sarvesh": 90,
#     "jery": 80
# }

passed_students = {student:score for (student, score) in students_scores.items() if score>=80}
# print(passed_students)

sentence = "What is the Airspeed Velocity of an Unladen Swallow?"
result = {word:len(word) for word in sentence.split()}
# print(result)

weather_c = {"Monday": 12, "Tuesday": 14, "Wednesday": 15, "Thursday": 14, "Friday": 21, "Saturday": 22, "Sunday": 24}
weather_f = {day:(cel * 9/5) + 32 for (day, cel) in weather_c.items()}
# print(weather_f)
