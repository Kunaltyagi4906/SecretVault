CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vault_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    secret_title TEXT,
    searchable_title TEXT,
    secret_data TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
