import pandas

data = pandas.read_csv("udemy/day25/weather_data.csv")
# print(type(data))
# print(type(data["temp"]))

# https://pandas.pydata.org/docs/reference/index.html ------- Pandas API refrences

data_dict = data.to_dict()
# print(data_dict)

temp_list = data["temp"].to_list()
# print(temp_list)

# average_temp = sum(temp_list) / len(temp_list)
# print(average_temp)

# print(data["temp"].mean())
# print(data["temp"].max())

# Get data in coloumns

# print(data["condition"])
# print(data.condition)

# Get data in rows

# print(data[data.day == "Monday"])
# print(data[data.temp == data.temp.max()])

# mondey = data[data.day == "Monday"]
# print(mondey.condition)

mondey = data[data.day == "Monday"]
mondey_temp = mondey.temp[0]
mondey_temp_feh = mondey.temp * 9/5 + 32
# print(mondey_temp_feh)

# Create a dataframe from scratch

data_dict = {
    "students": ["Sarvesh", "Chanchal", "Yogesh"],
    "scores": [90, 76, 55]
}
data = pandas.DataFrame(data_dict)
print(data)
data.to_csv(r"udemy\day25\new_data.csv")
