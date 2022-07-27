import bcrypt
from flask import Flask, render_template, url_for, request, session, redirect
from get_data import get_data
from to_bytes import to_bytes

app = Flask(__name__)

# Get data from database
numbers_users, numbers_orders, numbers_items, status_users, total_profit, item_ordered, users_list, image_users, db_users, db_umkm_lists = get_data()

@app.route('/')
def index():
    return render_template('index.html', numbers_users=numbers_users, numbers_orders=numbers_orders, numbers_items=numbers_items, status_users=status_users, total_profit=total_profit, item_ordered=item_ordered, users=users_list, image_users=image_users)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html', numbers_users=numbers_users, numbers_orders=numbers_orders, numbers_items=numbers_items, status_users=status_users, total_profit=total_profit, item_ordered=item_ordered, users=users_list, image_users=image_users, db_users=db_users, name_profile=session['username'])
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login_user = db_umkm_lists.find_one({'name' : request.form['username']})

        if login_user:
            if bcrypt.hashpw(to_bytes(request.form['pass']), to_bytes(login_user['password'])) == to_bytes(login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
        return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        existing_user = db_umkm_lists.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            db_umkm_lists.insert_one({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('login'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(port=5000)

    # for heroku
    # app.run(debug=True)