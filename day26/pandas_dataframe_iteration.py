student_dict = {
    "student": ['sarvesh', 'jery', 'aman', 'sunny', 'arya'],
    "score": [20, 21, 19, 22, 20],
}

# Looping through dictionaries
# for (key,value) in student_dict.items():
#   print(value)


import pandas

student_data_frame = pandas.DataFrame(student_dict)
# print(student_data_frame)

# LOOPING THROUGH PANDAS DATAFRAME

# for(key, value) in student_data_frame.items():
#     print(value)

# loop through rows of a data frame

for(index, row) in student_data_frame.iterrows():
    # print(row.student)
    if row.student == "sarvesh":
        print(row.score)
