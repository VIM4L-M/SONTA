from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_random_secret'

DATABASE = os.path.join(os.path.dirname(__file__), 'sonta.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    message = None
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        conn = get_db_connection()
        if action == 'signin':
            user = conn.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            if not user:
                error = 'No account with this username. Please sign up first.'
            elif user['password'] != password:
                error = 'Invalid password.'
            else:
                session['user_id'] = user['id']
                conn.close()
                return redirect(url_for('dashboard'))
        elif action == 'signup':
            try:
                conn.execute(
                    'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                    (username, email, password)
                )
                conn.commit()
                message = 'Sign up successful! Please sign in.'
            except sqlite3.IntegrityError:
                error = 'Username or email already exists'
        conn.close()
    return render_template('login.html', error=error, message=message)

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)