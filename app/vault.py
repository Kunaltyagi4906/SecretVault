from flask import Blueprint, render_template, request, redirect, session, flash
from config.db import get_db_connection
import csv
from flask import make_response

vault = Blueprint('vault', __name__)
import csv
from flask import make_response
from utils.crypto import encrypt_data, decrypt_data

@vault.route('/export')
def export_vault():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT secret_title, secret_data FROM vault_data WHERE user_id = %s", (session['user_id'],))
    secrets = cursor.fetchall()

    # Create CSV
    si = []
    si.append(['Title', 'Secret'])

    for row in secrets:
        si.append([row[0], row[1]])

    # Convert to response
    output = make_response('\n'.join([','.join(row) for row in si]))
    output.headers["Content-Disposition"] = "attachment; filename=secrets.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@vault.route('/vault')
def show_vault():
    print("🧠 Session check in /vault:", session)
    if 'user_id' not in session:
        print("🚫 No session, redirecting to login...")
        return redirect('/login')
    

    db = get_db_connection()
    cursor = db.cursor()

    search = request.args.get("q")
    page = int(request.args.get("page", 1))
    per_page = 5  # 🔁 Number of secrets per page
    offset = (page - 1) * per_page

    # 🔍 Count total secrets
    if search:
        cursor.execute("SELECT COUNT(*) FROM vault_data WHERE user_id = %s AND searchable_title LIKE %s", 
               (session['user_id'], f"%{search.lower()}%"))

    else:
        cursor.execute("SELECT COUNT(*) FROM vault_data WHERE user_id = %s", (session['user_id'],))
    
    total_secrets = cursor.fetchone()[0]
    total_pages = (total_secrets + per_page - 1) // per_page

    # 📦 Fetch paginated data
    if search:
        cursor.execute("SELECT id, secret_title, secret_data FROM vault_data WHERE user_id = %s AND searchable_title LIKE %s LIMIT %s OFFSET %s", 
               (session['user_id'], f"%{search.lower()}%", per_page, offset))

    else:
        cursor.execute("SELECT id, secret_title, secret_data FROM vault_data WHERE user_id = %s LIMIT %s OFFSET %s", 
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


@vault.route('/add', methods=['GET', 'POST'])
def add_secret():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()  # <-- THIS LINE is missing earlier!

    if request.method == 'POST':
        title = request.form['title']
        secret = request.form['secret']
        
        encrypted_secret = encrypt_data(secret)
        
        cursor = db.cursor()
        cursor.execute(
               "INSERT INTO vault_data (user_id, secret_title, searchable_title, secret_data) VALUES (%s, %s, %s, %s)",
                (session['user_id'], encrypt_data(title), title.lower(), encrypted_secret)
            )

        db.commit()
        flash('Secret added securely 🔐')
        return redirect('/vault')

    return render_template('add.html')

@vault.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_secret(id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        title = request.form['title']
        secret = request.form['secret']
        encrypted_title = encrypt_data(title)
        encrypted_secret = encrypt_data(secret)

        cursor.execute(
            "UPDATE vault_data SET secret_title = %s, searchable_title = %s, secret_data = %s WHERE id = %s AND user_id = %s",
            (encrypted_title, title.lower(), encrypted_secret, id, session['user_id'])
        )
        db.commit()
        flash('Updated successfully.')
        return redirect('/vault')

    cursor.execute("SELECT secret_title, secret_data FROM vault_data WHERE id = %s AND user_id = %s", (id, session['user_id']))
    data = cursor.fetchone()
    decrypted_title = decrypt_data(data[0])
    decrypted_secret = decrypt_data(data[1])
    return render_template('edit.html', title=decrypted_title, secret=decrypted_secret)


@vault.route('/delete/<int:id>')
def delete_secret(id):
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM vault_data WHERE id = %s AND user_id = %s", (id, session['user_id']))
    db.commit()
    flash('Deleted.')
    return redirect('/vault')
