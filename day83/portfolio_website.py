import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, g
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv(r'Python-udemy\day83\portfolio.env')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.getenv('DATABASE', os.path.join(BASE_DIR, 'portfolio.db'))
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')

app = Flask(__name__)

from flask_mail import Mail, Message

# ------------------ Email Config ------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Your email
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # App password

mail = Mail(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['DATABASE'] = DATABASE
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'images')
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB limit for uploads

# ------------------ Database helpers ------------------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    db.commit()


# ✅ Call the database init when app starts
with app.app_context():
    init_db()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# ------------------ Routes ------------------

projects_data = [
    {
        'id': 1,
        'title': 'Personal Blog Website',
        'description': 'A collection of random blogs.',
        'tech': ['Python', 'Tkinter', 'SQLite'],
        'image': 'project1.png',
        'link': 'https://blogs-ieyo.onrender.com/'
    },
    {
        'id': 2,
        'title': 'Smart Health Assistant',
        'description': 'Comprehensive healthcare management system integrating symptom analysis, patient records, and billing automation.',
        'tech': ['HTML', 'CSS', 'Flask'],
        'image': 'project2.png',
        'link': 'https://github.com/Sarveshsingh2007/Smart-Heath-Assistant'
    },
    {
        'id': 3,
        'title': 'Portfolio Backend',
        'description': 'This portfolio itself — built with Flask. Includes contact form and DB.',
        'tech': ['Flask', 'SQLite'],
        'image': 'project3.png',
        'link': 'https://www.linkedin.com/in/sarvesh-singh-6a8a152a6/'
    },
]


@app.route('/')
def index():
    return render_template('index.html', projects=projects_data)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects_data)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()

        if not name or not email or not message:
            flash('Please fill out all fields.', 'error')
            return redirect(url_for('contact'))

        # Save to DB
        db = get_db()
        cur = db.cursor()
        cur.execute('INSERT INTO messages (name, email, message, created_at) VALUES (?, ?, ?, ?)',
                    (name, email, message, datetime.utcnow().isoformat()))
        db.commit()

        # 📧 Send email to admin
        try:
            msg = Message(
                subject=f"New Contact Message from {name}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],  # Send to yourself (admin)
                body=f"📩 New message from your portfolio site:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"
            )
            mail.send(msg)
            flash('Thanks! Your message has been received and emailed.', 'success')
        except Exception as e:
            flash(f"Message saved, but email failed: {e}", 'warning')

        return redirect(url_for('index'))

    return render_template('contact.html')



@app.route('/admin/messages')
def admin_messages():
    # Simple admin page to view messages. In a real app, protect with auth.
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM messages ORDER BY created_at DESC')
    rows = cur.fetchall()
    return render_template('admin_messages.html', messages=rows)


if __name__ == '__main__':
    app.run(debug=True)