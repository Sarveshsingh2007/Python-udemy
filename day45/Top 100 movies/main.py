import requests
from bs4 import BeautifulSoup

response = requests.get("https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/")
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")


all_movies = soup.find_all("h3", class_="title")

movie_titles = [movie.get_text() for movie in all_movies]
movie_titles.reverse()

with open(r'udemy\day45\top 100 movies\top_100_movies.txt', 'w', encoding="utf-8") as file:
    for movie in movie_titles:
        file.write(movie + "\n")
