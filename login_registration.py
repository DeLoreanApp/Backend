from fastapi import FastAPI
import sqlite3

from flask import jsonify


app = FastAPI()


@app.post("/login")
async def login(username, password):
    conn = sqlite3.connect('user.db')
    curser_obj = conn.cursor()
    curser_obj.execute(f"SELECT * FROM users WHERE username='{username}' AND password= '{password}'")
    conn.commit()
    number_of_rows = 0
    return_data = None
    for line in curser_obj:
        return_data = line
        number_of_rows += 1
    if number_of_rows == 1:
        return jsonify({'status': 'success', 'data': return_data})
    else:
        return jsonify({'status': 'fail', 'data': None})
    conn.close()


@app.post("/register")
async def register(first_name, username, password):
    if '@' not in username:
        return jsonify({'error': 'Invalid email address'})
    connection = sqlite3.connect('user.db')
    curser_obj = connection.cursor()
    curser_obj.execute(f"SELECT count(*) FROM users WHERE username = '{username}' ")
    connection.commit()
    if curser_obj.fetchone()[0] == 1:
        return jsonify({'error': 'User already exists'})
    else:
        curser_obj.execute('INSERT INTO users VALUES (NULL,?, ?, ?)', (first_name, username, password))
        connection.commit()
        data = jsonify(curser_obj)
        connection.close()
        return data
