import requests 
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "2BILEIB2LK6B8TJK"
NEWS_API_KEY = "b6556b78833c478fbdcb12ad29aace58"

TWILIO_SID = ""
TWILIO_AUTH = ""
MY_NUMBER = ""
RECIVER_NUMBER = ""

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
# print(yesterday_closing_price)


day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
# print(day_before_yesterday_closing_price)


difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
# print(diff_percent)

if abs(diff_percent) >= 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    # print(three_articles)


    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}% \nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    # print(formatted_articles)


    client = Client(TWILIO_SID, TWILIO_AUTH)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=MY_NUMBER,
            to=RECIVER_NUMBER
        )
    print(f"Message sent: {message.sid}")
    print(f"Status: {message.status}")
    print(f"To: {message.to}")
    print(f"From: {message.from_}")
    print(f"Error Code: {message.error_code}")
    print(f"Error Message: {message.error_message}")
