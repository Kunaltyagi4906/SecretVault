# 🔐 My Vault  

A **secure password manager** built with Flask, SQLite, and modern UI (glassmorphism + gradient effects).  
Easily register, login, and store your secrets safely inside your own vault.  

---

## 🚀 Features
- 🧑‍💻 User authentication (Register/Login)
- 🔑 AES-based encryption for secrets
- 📂 Vault to store & manage secrets
- ✨ Glassmorphic UI with gradient animations
- 🔍 Search + pagination for stored items
- 📱 Fully responsive design
- 🔒 Sensitive data never exposed in plain text

---

## 🗂️ Project Structure
├── app/ # Flask routes, auth, vault logic
├── config/ # Database connection
├── utils/ # Crypto, validators, filters
├── static/ # CSS & frontend assets
├── templates/ # Jinja2 HTML templates
├── app.py # Main Flask entry
├── schema.sql # Database schema
├── requirements.txt # Python dependencies
├── Dockerfile # For container deployment
└── README.md # Documentation


---

## ⚙️ Setup & Installation  

### 1️⃣ Clone Repo
```bash
git clone https://github.com/YOUR_USERNAME/my-vault.git
cd my-vault


python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows


pip install -r requirements.txt
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database.db

