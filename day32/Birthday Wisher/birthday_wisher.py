from datetime import datetime
import pandas
import random
import smtplib

MY_EMAIL = "sarveshsingh9381@gmail.com"
MY_PASSWORD = "dnnf pxsv zmmr szjw"


today = datetime.now()
today_tuple = (today.month, today.day)

data = pandas.read_csv(r"udemy\day32\Birthday_wisher\birthdays.csv")
birthday_dict = {(data_row["month"], data_row["day"]): data_row for (index, data_row) in data.iterrows()}


if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple]
    file_path = f"udemy/day32/Birthday_wisher/letter_templates/letter_{random.randint(1,3)}.txt"

    with open (file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace("[NAME]", birthday_person["name"])

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL, 
            to_addrs=birthday_person["email"], 
            msg = f"Subject: Happy Birthday!\n\n{contents}"
        )
print("Mail sent successfully!")
