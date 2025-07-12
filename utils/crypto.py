# utils/crypto.py
from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

cipher = Fernet(load_key())

def encrypt_data(data):
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    return cipher.decrypt(encrypted_data.encode()).decode()
