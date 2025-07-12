import os

folders = [
    "app", "templates", "static", "config"
]
files = [
    "run.py", "requirements.txt",
    "app/__init__.py", "app/routes.py", "app/auth.py", "app/vault.py", "app/utils.py",
    "config/db.py",
    "templates/login.html", "templates/register.html", "templates/vault.html", "templates/add.html", "templates/edit.html",
    "static/styles.css"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, 'w') as f:
        f.write("# " + file)

print("🔥 Project structure ready!")
