from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import os

APP_DB = "cafes.db"
DEBUG = True
SECRET_KEY = "python-udemy-day-88-secret-key"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = app.config["SECRET_KEY"]


# ---------- Database Functions ----------

def get_db_connection():
    conn = sqlite3.connect(APP_DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create table if it doesn't exist (no sample data added)."""
    conn = get_db_connection()
    cur = conn.cursor()

    # ✅ Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cafes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            map_url TEXT,
            img_url TEXT,
            location TEXT,
            has_socket INTEGER DEFAULT 0,
            has_toilet INTEGER DEFAULT 0,
            has_wifi INTEGER DEFAULT 0,
            can_take_calls INTEGER DEFAULT 0,
            seats TEXT,
            coffee_price TEXT
        );
    """)
    conn.commit()

    print("✅ Database ready — 'cafes' table created (if it didn’t exist).")
    conn.close()



# ✅ Initialize DB on startup
init_db()


# ---------- Web Routes ----------

@app.route("/")
def index():
    conn = get_db_connection()
    cafes = conn.execute("SELECT * FROM cafes ORDER BY id DESC;").fetchall()
    conn.close()
    return render_template("index.html", cafes=cafes)


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        map_url = request.form.get("map_url", "").strip()
        img_url = request.form.get("img_url", "").strip()
        location = request.form.get("location", "").strip()
        has_socket = 1 if request.form.get("has_socket") == "on" else 0
        has_toilet = 1 if request.form.get("has_toilet") == "on" else 0
        has_wifi = 1 if request.form.get("has_wifi") == "on" else 0
        can_take_calls = 1 if request.form.get("can_take_calls") == "on" else 0
        seats = request.form.get("seats", "").strip()
        coffee_price = request.form.get("coffee_price", "").strip()

        if not name:
            flash("⚠️ Cafe name is required.", "error")
            return redirect(url_for("add_cafe"))

        conn = get_db_connection()
        conn.execute("""
            INSERT INTO cafes 
            (name, map_url, img_url, location, has_socket, has_toilet, has_wifi, can_take_calls, seats, coffee_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, map_url, img_url, location, has_socket, has_toilet, has_wifi, can_take_calls, seats, coffee_price))
        conn.commit()
        conn.close()

        flash("✅ Cafe added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<int:cafe_id>", methods=["POST"])
def delete_cafe(cafe_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cafes WHERE id = ?", (cafe_id,))
    row = cur.fetchone()
    if row:
        cur.execute("DELETE FROM cafes WHERE id = ?", (cafe_id,))
        conn.commit()
        flash("✅ Cafe deleted.", "success")
    else:
        flash("⚠️ Cafe not found.", "error")
    conn.close()
    return redirect(url_for("index"))


# ---------- REST API ----------

@app.route("/api/cafes", methods=["GET"])
def api_get_cafes():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM cafes ORDER BY id DESC;").fetchall()
    conn.close()
    cafes = [dict(r) for r in rows]

    # Convert integer booleans to real booleans
    for c in cafes:
        c["has_socket"] = bool(c["has_socket"])
        c["has_toilet"] = bool(c["has_toilet"])
        c["has_wifi"] = bool(c["has_wifi"])
        c["can_take_calls"] = bool(c["can_take_calls"])

    return jsonify(cafes)


@app.route("/api/cafes/<int:cafe_id>", methods=["GET"])
def api_get_cafe(cafe_id):
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM cafes WHERE id = ?", (cafe_id,)).fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "Cafe not found"}), 404

    cafe = dict(row)
    cafe["has_socket"] = bool(cafe["has_socket"])
    cafe["has_toilet"] = bool(cafe["has_toilet"])
    cafe["has_wifi"] = bool(cafe["has_wifi"])
    cafe["can_take_calls"] = bool(cafe["can_take_calls"])
    return jsonify(cafe)


# ---------- Run Server ----------

if __name__ == "__main__":
    app.run(debug=DEBUG)
