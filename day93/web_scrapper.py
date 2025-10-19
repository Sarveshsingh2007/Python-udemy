import requests
from bs4 import BeautifulSoup
import csv
import time

# URL of Steam Top Sellers page
url = "https://store.steampowered.com/search/?filter=topsellers"

# Send GET request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code != 200:
    print("❌ Failed to fetch the page. Status code:", response.status_code)
    exit()

# Parse the page with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find all game blocks
games = soup.find_all("a", class_="search_result_row")

# List to store data
data = []

# Extract data for each game
for game in games:
    title_tag = game.find("span", class_="title")
    release_tag = game.find("div", class_="search_released")
    price_tag = game.find("div", class_="search_price")
    review_tag = game.find("span", class_="search_review_summary")

    title = title_tag.text.strip() if title_tag else "N/A"
    release_date = release_tag.text.strip() if release_tag else "N/A"
    price = price_tag.text.strip().replace("\r", "").replace("\n", "") if price_tag else "N/A"
    review = review_tag["data-tooltip-html"] if review_tag else "No reviews"

    data.append([title, release_date, price, review])

    # (Optional) Wait a bit to be polite to server
    time.sleep(0.1)

# Save to CSV
filename = r"Python-udemy\day93\steam_games.csv"
with open(filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Release Date", "Price", "Review Summary"])
    writer.writerows(data)

print(f"✅ Scraping complete! Data saved to '{filename}'")
