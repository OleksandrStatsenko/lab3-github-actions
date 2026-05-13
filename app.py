from flask import Flask, request, escape
import sqlite3
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "Secure Flask App"

# Захищений login
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

    with open(filename, 'r') as f:
        return f.read()

# Захист від Command Injection
@app.route('/run')
def run():
    cmd = request.args.get('cmd', '')

    allowed_commands = ['date', 'whoami']

    if cmd not in allowed_commands:
        return "Command not allowed"

    result = subprocess.run(
        [cmd],
        capture_output=True,
        text=True
    )

    return result.stdout

if __name__ == '__main__':
    app.run(debug=True)
