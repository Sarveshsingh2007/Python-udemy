from bs4 import BeautifulSoup
import requests

response = requests.get("https://news.ycombinator.com/news")
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

articles = soup.find_all("span", class_="titleline")
article_texts = []
article_links = []

for article_tag in articles:
    a_tag = article_tag.find("a")
    text = a_tag.get_text()
    link = a_tag.get("href")
    article_texts.append(text)
    article_links.append(link)



article_upvotes = [int(score.get_text().split()[0]) for score in soup.find_all("span", class_="score")]

# print(article_texts)
# print(article_links)
# print(article_upvotes)

max_upvote = max(article_upvotes)
max_index = article_upvotes.index(max_upvote)

print("----Article with Highest upvote----")
print("Title: ", article_texts[max_index])
print("Link: ", article_links[max_index])
print("Upvote: ", max_upvote)
