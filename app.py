from turtle import title
from flask import Flask, request, jsonify, send_file, Flask, session, render_template, redirect, g, url_for
from psycopg2 import connect, extras
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv
from os import environ

load_dotenv()

app = Flask(__name__)

# Login secret
app.secret_key = os.urandom(24)

# cifrar contraseña
key = Fernet.generate_key()

# connect
host = environ.get('DB_HOST')
port = environ.get('DB_PORT')
dbname = environ.get('DB_NAME')
user = environ.get('DB_USER')
password = environ.get('DB_PASSWORD')


def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                   user=user, password=password)
    return conn


@app.get('/api/tasks')
def get_tasks():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM task')
    tasks = cur.fetchall()

    print(tasks)

    cur.close()
    conn.close()

    return jsonify(tasks)


@app.post('/api/tasks')
def create_task():
    new_task = request.get_json()
    title = new_task['title']
    task = new_task['task']
    # encripto psw
    print(title, task)

    conn = get_connection()
    # RealDictCursor convierte la respuesta en tuplas/filas
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    # genero una consulta con variables
    cur.execute('INSERT INTO task (title, task) VALUES (%s, %s) RETURNING *',
                (title, task))

    new_created_task = cur.fetchone()
    print(new_created_task)

    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_created_task)


@app.delete('/api/tasks/<id>')
def delete_task(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    # delete task
    cur.execute('DELETE FROM task WHERE id = %s RETURNING * ', (id,))

    # traigo la tarea eliminada
    task = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    if task is None:
        return jsonify({"message": "Task not found"}), 404
    print(task)
    return jsonify(task)


@app.put('/api/tasks/<id>')
def update_task(id):

    conn = get_connection()
    # RealDictCursor convierte la respuesta en tuplas/filas
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_task = request.get_json()
    title = new_task['title']
    task = new_task['task']
    # password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8')) # Encripto contraseña

    cur.execute(
        'UPDATE task SET title=%s, task = %s WHERE id = %s RETURNING *', (title, task, id)
        )
    update_task = cur.fetchone()
    conn.commit()
    print(update_task)

    cur.close()
    conn.close()
    if update_task is None:
        return jsonify({'message': 'Task not found'}), 404

    print(update_task)
    return jsonify(update_task)


@app.get('/api/tasks/<id>')
def get_task(id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM task WHERE id = %s', (id,))
    task = cur.fetchone()

    if task is None:
        return jsonify({'message': 'task not found'}), 404

    return jsonify(task)

# @app.get('/crud')
# def home():
#     return send_file('static/protected.html')

# Login

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        session.pop('users', None)

        if request.form['password'] == 'vladimir':
            session['user'] = request.form['username']
            return redirect(url_for('protected'))

    return render_template('index.html')

@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html', user = session['user'])
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None

    if 'user' in session:
        g.user = session['user']

@app.route('/dropsession')
def dropsession():
    session.clear()
    return render_template(('index.html'))



if __name__ == '__main__':
    app.run(debug=True)
