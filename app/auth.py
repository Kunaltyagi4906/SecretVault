import re
from utils.validators import is_strong_password

from flask import Blueprint, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from config.db import get_db_connection

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password_raw = request.form['password']

        if not is_strong_password(password_raw):
            flash('Password must be 8+ chars, with uppercase, number, and special char!')
            return redirect('/register')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email format!")
            return redirect('/register')

        password = generate_password_hash(password_raw)

        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            db.commit()
            flash('Registration successful! 📧')
            return redirect('/login')
        except:
            flash('Username or email already exists 😬')
            return redirect('/register')

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password_input):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect('/vault')
        else:
            flash('Invalid credentials.')
            return redirect('/login')

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect('/login')
