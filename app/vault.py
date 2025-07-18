from flask import Blueprint, render_template, request, redirect, session, flash, make_response
from config.db import get_db_connection
from utils.crypto import encrypt_data, decrypt_data
import csv

vault = Blueprint('vault', __name__)

# 🔐 Export secrets to CSV
@vault.route('/export')
def export_vault():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()

    # SQLite/MySQL support
    placeholder = "?" if db.__class__.__module__.startswith("sqlite3") else "%s"
    cursor.execute(f"SELECT secret_title, secret_data FROM vault_data WHERE user_id = {placeholder}", (session['user_id'],))
    secrets = cursor.fetchall()

    # 🧾 CSV content
    csv_rows = [["Title", "Secret"]]
    for row in secrets:
        title = decrypt_data(row[0])
        secret = decrypt_data(row[1])
        csv_rows.append([title, secret])

    # 📤 Send CSV as response
    csv_output = "\n".join([",".join(row) for row in csv_rows])
    response = make_response(csv_output)
    response.headers["Content-Disposition"] = "attachment; filename=secrets.csv"
    response.headers["Content-type"] = "text/csv"
    return response

# 📂 Vault Dashboard
@vault.route('/vault')
def show_vault():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()

    search = request.args.get("q")
    page = int(request.args.get("page", 1))
    per_page = 5
    offset = (page - 1) * per_page
    placeholder = "?" if db.__class__.__module__.startswith("sqlite3") else "%s"

    # 🧮 Total count
    if search:
        cursor.execute(f"SELECT COUNT(*) FROM vault_data WHERE user_id = {placeholder} AND searchable_title LIKE {placeholder}",
                       (session['user_id'], f"%{search.lower()}%"))
    else:
        cursor.execute(f"SELECT COUNT(*) FROM vault_data WHERE user_id = {placeholder}", (session['user_id'],))
    
    total_secrets = cursor.fetchone()[0]
    total_pages = (total_secrets + per_page - 1) // per_page

    # 📦 Fetch paginated secrets
    if search:
        cursor.execute(f"SELECT id, secret_title, secret_data FROM vault_data WHERE user_id = {placeholder} AND searchable_title LIKE {placeholder} LIMIT {placeholder} OFFSET {placeholder}",
                       (session['user_id'], f"%{search.lower()}%", per_page, offset))
    else:
        cursor.execute(f"SELECT id, secret_title, secret_data FROM vault_data WHERE user_id = {placeholder} LIMIT {placeholder} OFFSET {placeholder}",
                       (session['user_id'], per_page, offset))

    secrets = cursor.fetchall()
    decrypted_secrets = [(id, decrypt_data(title), decrypt_data(secret)) for (id, title, secret) in secrets]

    cursor.close()
    db.close()

    return render_template('vault.html',
                           username=session.get("username"),
                           secrets=decrypted_secrets,
                           search=search,
                           page=page,
                           total_pages=total_pages)

# ➕ Add secret
@vault.route('/add', methods=['GET', 'POST'])
def add_secret():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()
    placeholder = "?" if db.__class__.__module__.startswith("sqlite3") else "%s"

    if request.method == 'POST':
        title = request.form['title']
        secret = request.form['secret']

        encrypted_title = encrypt_data(title)
        encrypted_secret = encrypt_data(secret)

        cursor.execute(f"INSERT INTO vault_data (user_id, secret_title, searchable_title, secret_data) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})",
                       (session['user_id'], encrypted_title, title.lower(), encrypted_secret))
        db.commit()
        flash("Secret added securely 🔐")
        return redirect('/vault')

    return render_template('add.html')

# ✏️ Edit secret
@vault.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_secret(id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()
    placeholder = "?" if db.__class__.__module__.startswith("sqlite3") else "%s"

    if request.method == 'POST':
        title = request.form['title']
        secret = request.form['secret']
        encrypted_title = encrypt_data(title)
        encrypted_secret = encrypt_data(secret)

        cursor.execute(f"UPDATE vault_data SET secret_title = {placeholder}, searchable_title = {placeholder}, secret_data = {placeholder} WHERE id = {placeholder} AND user_id = {placeholder}",
                       (encrypted_title, title.lower(), encrypted_secret, id, session['user_id']))
        db.commit()
        flash("Updated successfully ✅")
        return redirect('/vault')

    cursor.execute(f"SELECT secret_title, secret_data FROM vault_data WHERE id = {placeholder} AND user_id = {placeholder}",
                   (id, session['user_id']))
    data = cursor.fetchone()

    if data:
        decrypted_title = decrypt_data(data[0])
        decrypted_secret = decrypt_data(data[1])
        return render_template('edit.html', title=decrypted_title, secret=decrypted_secret)
    else:
        flash("Secret not found 🤔")
        return redirect('/vault')

# 🗑️ Delete secret
@vault.route('/delete/<int:id>')
def delete_secret(id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()
    placeholder = "?" if db.__class__.__module__.startswith("sqlite3") else "%s"

    cursor.execute(f"DELETE FROM vault_data WHERE id = {placeholder} AND user_id = {placeholder}",
                   (id, session['user_id']))
    db.commit()
    flash("Secret deleted 🗑️")
    return redirect('/vault')
