from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from utils.validators import is_strong_password
import sqlite3

auth = Blueprint('auth', __name__)

# 🔐 Database utility
def get_db():
    conn = sqlite3.connect('vault.db')
    conn.row_factory = sqlite3.Row
    return conn

# 🔐 Register Route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_strong_password(password):
            flash("Password must be at least 8 chars, include uppercase, lowercase, number, and special char ⚠️", "error")
            return redirect(url_for('auth.register'))

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            flash("Username already exists! Try logging in instead 😅", "error")
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password)
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        flash("Registration successful! Now log in 🚀", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# 🔐 Login Route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session.permanent = True
            flash("Welcome back! 🎉", "success")
            return redirect(url_for('vault.dashboard'))
        else:
            flash("Invalid username or password 😓", "error")
            return redirect(url_for('auth.login'))

    return render_template('login.html')

# 🚪 Logout Route
@auth.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully 👋", "info")
    return redirect(url_for('auth.login'))
