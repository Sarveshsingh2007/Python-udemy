from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

SENTENCES = [
    "Practice makes perfect when it comes to typing.",
    "Typing speed tests help improve your accuracy and speed.",
    "Consistency is the key to mastering typing skills.",
    "Accuracy matters more than speed when learning to type.",
    "Fast typing helps improve productivity and save time."
]

@app.route("/")
def index():
    sentence = random.choice(SENTENCES)
    return render_template("index.html", sentence=sentence)

@app.route("/new_sentence")
def new_sentence():
    return jsonify({"sentence": random.choice(SENTENCES)})

if __name__ == "__main__":
    app.run(debug=True)
