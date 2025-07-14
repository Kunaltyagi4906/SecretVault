from flask import Blueprint, redirect

main = Blueprint('main', __name__)
@main.route('/')
def home():
    if 'user_id' in session:
        return redirect('/vault')
    return redirect('/login')


