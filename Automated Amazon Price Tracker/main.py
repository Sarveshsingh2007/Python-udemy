import requests
from bs4 import BeautifulSoup
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=r"udemy\day47\requirement.env")


# Scrape price
url = "https://appbrewery.github.io/instant_pot/"

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}


response = requests.get(url, headers=header)
soup = BeautifulSoup(response.text, "html.parser")

price = soup.find(class_="a-offscreen").get_text()
price_as_float = float(price.split("$")[1])
# print(price_as_float)

# Email if price drops below threshold
if price_as_float < 100.00:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(
            user=os.getenv("EMAIL_ADDRESS"),
            password=os.getenv("EMAIL_PASSWORD")
        )
        connection.sendmail(
            from_addr=os.getenv("EMAIL_ADDRESS"),
            to_addrs="sarveshadhikari905@gmail.com",
            msg=f"Subject:Instant Pot Price Drop!\n\nThe price is now ${price_as_float}. Buy now: {url}"
        )
        print("✅ Email sent successfully.")
else:
    print("ℹ️ Price is still above $100.")
