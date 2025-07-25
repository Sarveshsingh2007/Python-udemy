import smtplib
import datetime as dt
import random

now = dt.datetime.now()
weekday = now.weekday()
if weekday == 4:
    with open (r"udemy\day32\quotes.txt") as all_quotes:
        all_quotes = all_quotes.readlines()
        quote = random.choice(all_quotes)


    my_email = "sarveshsingh9381@gmail.com"
    password = "ltjm ebqr myyt ijuj"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs="sarveshadhikari905@gmail.com",
            msg= f"Subject: Firday Motivation\n\n{quote}"
        )
