import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="udemy/day47/requirement.env")

url = "https://www.amazon.in/iPhone-16-256-GB-Control/dp/B0DGJKT2V7/ref=sr_1_2_sspa?sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept-Language": "en-US,en;q=0.9",
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price = soup.find(class_="a-offscreen").get_text()
price_as_float = float(price.split("₹")[1].replace(",", ""))
# print(price_as_float)

if price_as_float < 100000.0:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(
            user=os.getenv("EMAIL_ADDRESS"),
            password=os.getenv("EMAIL_PASSWORD")
        )
        connection.sendmail(
            from_addr=os.getenv("EMAIL_ADDRESS"),
            to_addrs="sarveshadhikari905@gmail.com",
            msg=f"Subject:Iphone 16 Price Drop!\n\nThe price is now ₹{price_as_float}. Buy now: {url}"
        )
        print("✅ Email sent successfully.")
