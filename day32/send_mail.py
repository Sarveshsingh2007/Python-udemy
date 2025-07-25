import smtplib

my_email = "sarveshsingh9381@gmail.com"
password = "ngri wunl ubtf bnlw"
with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email, 
        to_addrs="monikaadhikari2001@gmail.com", 
        msg="Subject:Hello\n\nHow are you my friend")

# import datetime as dt

# now = dt.datetime.now()
# year = now.year
# weekday = now.weekday()
# month = now.month
# if year == 2022:
#     print("Work hard you have not much time.")
# else:
#     print(f"this is {weekday} day of week you can take rest")

# date_of_birth = dt.datetime(year=2005, month=9, day=10, hour=5)
# print(date_of_birth)
