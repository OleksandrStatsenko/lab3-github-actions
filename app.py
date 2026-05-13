from flask import Flask, request
from markupsafe import escape
import sqlite3
import subprocess

app = Flask(__name__)

# Автоматичне створення БД
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)

    cursor.execute("DELETE FROM users")

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "password")
    )

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return "Secure Flask App"

# Захист від SQL Injection
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username=? AND password=?"

    cursor.execute(query, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        return "Вітаємо!"

    return "Невірні дані"

# Захист від XSS
@app.route('/profile')
def profile():
    name = request.args.get('name', '')
    return escape(name)

# Захист від Path Traversal
@app.route('/file')
def file():
    filename = request.args.get('name', '')

    allowed_files = ['test.txt']

    if filename not in allowed_files:
        return "Access denied"

    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"

# Захист від Command Injection
@app.route('/run')
def run():
    cmd = request.args.get('cmd', '')

    allowed_commands = {
        'date': ['date'],
        'whoami': ['whoami']
    }

    if cmd not in allowed_commands:
        return "Command not allowed"

    result = subprocess.run(
        allowed_commands[cmd],
        capture_output=True,
        text=True
    )

    return result.stdout

if __name__ == '__main__':
    app.run(debug=False)
