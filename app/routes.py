@main.route('/')
def home():
    if 'user_id' in session:
        return redirect('/vault')
    return redirect('/login')
