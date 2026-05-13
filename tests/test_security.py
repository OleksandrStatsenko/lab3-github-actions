import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

client = app.test_client()


def test_sql_injection():
    response = client.post('/login', data={
        'username': "admin' --",
        'password': '123'
    })

    assert 'Вітаємо!' not in response.get_data(as_text=True)


def test_xss():
    response = client.get('/profile?name=<script>alert(1)</script>')

    assert '<script>' not in response.get_data(as_text=True)


def test_path_traversal():
    response = client.get('/file?name=../../etc/passwd')

    assert 'root:' not in response.get_data(as_text=True)


def test_command_injection():
    response = client.get('/run?cmd=ls;cat /etc/passwd')

    assert 'root:' not in response.get_data(as_text=True)
