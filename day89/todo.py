"""
Single-file Flask Todo App
- Save this file as `flask_todo_app.py`
- Requirements: Flask (pip install flask)
- Run: python flask_todo_app.py
- Opens at http://127.0.0.1:5000

Features:
- Add / edit / delete tasks
- Mark tasks complete / incomplete
- Filter: All / Active / Completed
- Persistent storage via SQLite (file: todos.db)
- Minimal, responsive UI (Bootstrap CDN)

This file uses render_template_string to keep everything in one file for easy sharing.
"""

from flask import Flask, request, redirect, url_for, g, render_template_string, flash
import sqlite3
from datetime import datetime
import os

DB_PATH = r'Python-udemy\day89\todos.db'

app = Flask(__name__)
app.secret_key = 'dev-secret-key'  # change for production

# ---------- Database helpers ----------

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        need_init = not os.path.exists(DB_PATH)
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
        if need_init:
            init_db(db)
    return db


def init_db(db):
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    ''')
    db.commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ---------- CRUD operations ----------

def add_task(title):
    db = get_db()
    db.execute('INSERT INTO tasks (title, created_at) VALUES (?, ?)',
               (title.strip(), datetime.utcnow().isoformat()))
    db.commit()


def update_task(task_id, title=None, done=None):
    db = get_db()
    if title is not None and done is not None:
        db.execute('UPDATE tasks SET title = ?, done = ? WHERE id = ?', (title, done, task_id))
    elif title is not None:
        db.execute('UPDATE tasks SET title = ? WHERE id = ?', (title, task_id))
    elif done is not None:
        db.execute('UPDATE tasks SET done = ? WHERE id = ?', (done, task_id))
    db.commit()


def delete_task(task_id):
    db = get_db()
    db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    db.commit()


def get_tasks(filter_mode='all'):
    db = get_db()
    if filter_mode == 'active':
        cur = db.execute('SELECT * FROM tasks WHERE done = 0 ORDER BY id DESC')
    elif filter_mode == 'completed':
        cur = db.execute('SELECT * FROM tasks WHERE done = 1 ORDER BY id DESC')
    else:
        cur = db.execute('SELECT * FROM tasks ORDER BY id DESC')
    return cur.fetchall()

# ---------- Routes ----------

BASE_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Simple Todo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body { padding-top: 40px; }
      .task-done { text-decoration: line-through; opacity: 0.6; }
      .task-row { transition: background-color .12s ease; }
      .small-muted { font-size: .85rem; color: #6c757d; }
    </style>
  </head>
  <body>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-12 col-md-8 col-lg-7">
        <h1 class="mb-3">✅ My Todo</h1>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for m in messages %}
              <div class="alert alert-info alert-sm">{{ m }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <form method="POST" action="{{ url_for('add') }}" class="mb-3">
          <div class="input-group">
            <input name="title" required placeholder="Add a new task..." class="form-control" autofocus>
            <button class="btn btn-primary">Add</button>
          </div>
        </form>

        <div class="d-flex justify-content-between align-items-center mb-2">
          <div>
            <a href="{{ url_for('index', filter='all') }}" class="me-2{% if active_filter=='all' %} fw-bold{% endif %}">All</a>
            <a href="{{ url_for('index', filter='active') }}" class="me-2{% if active_filter=='active' %} fw-bold{% endif %}">Active</a>
            <a href="{{ url_for('index', filter='completed') }}" class="me-2{% if active_filter=='completed' %} fw-bold{% endif %}">Completed</a>
          </div>
          <div class="small-muted">{{ tasks|length }} tasks</div>
        </div>

        <ul class="list-group">
          {% for t in tasks %}
          <li class="list-group-item task-row d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center gap-2">
              <form method="POST" action="{{ url_for('toggle', task_id=t['id']) }}">
                <button class="btn btn-sm btn-outline-secondary" title="Toggle complete">{% if t['done'] %}🔁{% else %}✔️{% endif %}</button>
              </form>

              <div class="ms-2">
                <div class="{% if t['done'] %}task-done{% endif %}">{{ t['title'] }}</div>
                <div class="small-muted">Created: {{ t['created_at'][:19].replace('T',' ') }}</div>
              </div>
            </div>

            <div class="btn-group">
              <a href="{{ url_for('edit', task_id=t['id']) }}" class="btn btn-sm btn-outline-primary">Edit</a>
              <form method="POST" action="{{ url_for('delete', task_id=t['id']) }}" onsubmit="return confirm('Delete this task?');">
                <button class="btn btn-sm btn-outline-danger">Delete</button>
              </form>
            </div>
          </li>
          {% else %}
          <li class="list-group-item text-muted">No tasks yet — add your first one!</li>
          {% endfor %}
        </ul>

        <footer class="mt-4 text-muted small">Tip: Use filters to focus. This app stores data in <code>todos.db</code> beside the script.</footer>
      </div>
    </div>
  </div>
  </body>
</html>
'''

EDIT_TEMPLATE = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Edit Task</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body>
  <div class="container" style="padding-top:40px;">
    <div class="row justify-content-center">
      <div class="col-12 col-md-8 col-lg-6">
        <h2>Edit Task</h2>
        <form method="POST">
          <div class="mb-3">
            <label class="form-label">Title</label>
            <input name="title" class="form-control" required value="{{ task['title'] }}">
          </div>
          <div class="mb-3 form-check">
            <input type="checkbox" name="done" class="form-check-input" id="done" {% if task['done'] %}checked{% endif %}>
            <label class="form-check-label" for="done">Completed</label>
          </div>
          <button class="btn btn-primary">Save</button>
          <a class="btn btn-secondary" href="{{ url_for('index') }}">Cancel</a>
        </form>
      </div>
    </div>
  </div>
  </body>
</html>
'''

@app.route('/')
def index():
    filter_mode = request.args.get('filter', 'all')
    tasks = get_tasks(filter_mode)
    return render_template_string(BASE_TEMPLATE, tasks=tasks, active_filter=filter_mode)


@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if not title:
        flash('Task cannot be empty.')
    else:
        add_task(title)
        flash('Added task.')
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle(task_id):
    db = get_db()
    cur = db.execute('SELECT done FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if cur is None:
        flash('Task not found.')
    else:
        new_done = 0 if cur['done'] else 1
        update_task(task_id, done=new_done)
        flash('Toggled task status.')
    return redirect(request.referrer or url_for('index'))


@app.route('/delete/<int:task_id>', methods=['POST'])
def delete(task_id):
    delete_task(task_id)
    flash('Deleted task.')
    return redirect(request.referrer or url_for('index'))


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit(task_id):
    db = get_db()
    task = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    if task is None:
        flash('Task not found.')
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        done = 1 if request.form.get('done') == 'on' else 0
        if not title:
            flash('Title cannot be empty.')
        else:
            update_task(task_id, title=title, done=done)
            flash('Task updated.')
            return redirect(url_for('index'))

    return render_template_string(EDIT_TEMPLATE, task=task)


if __name__ == '__main__':
    app.run(debug=True)
