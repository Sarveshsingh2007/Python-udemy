from flask import Flask, render_template, request
import requests
from livereload import Server   # <-- NEW LINE

app = Flask(__name__)

API_URL = "https://hp-api.onrender.com/api/characters"

@app.route("/", methods=["GET", "POST"])
def index():
    search_query = ""
    house_filter = ""
    try:
        response = requests.get(API_URL)
        characters = response.json()
    except Exception as e:
        characters = []
        print("Error fetching data:", e)

    if request.method == "POST":
        search_query = request.form.get("search", "").strip().lower()
        house_filter = request.form.get("house", "").strip().lower()

        characters = [
            c for c in characters
            if (search_query in c.get("name", "").lower())
            and (not house_filter or (c.get("house", "") or "").lower() == house_filter)
        ]

    return render_template("index.html",
                           characters=characters,
                           search_query=search_query,
                           house_filter=house_filter)

@app.route("/character/<name>")
def character(name):
    try:
        response = requests.get(API_URL)
        data = response.json()
        character = next((c for c in data if c["name"].lower() == name.lower()), None)
    except Exception as e:
        print("Error:", e)
        character = None

    return render_template("character.html", character=character)

@app.route("/about")
def about():
    return render_template("about.html")

# ==============================
# AUTO RELOAD ENABLED HERE 🔥
# ==============================
if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.watch('templates/*.html')   # Watch all your HTML files
    server.watch('static/*.css')       # Watch CSS files
    server.watch('app.py')             # Watch the main Python file
    server.serve(debug=True, port=5000)
