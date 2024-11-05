from flask import Flask, render_template, request, redirect, session
import sqlite3
from functools import wraps

app = Flask(__name__, template_folder='templates')
app.secret_key = 'asdasdasda12122'


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return wrapper
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class first_database():
    def __init__(self, file_name):
        self.con = sqlite3.connect(file_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with first_database('db1.db') as db_cur:
            db_cur.execute(
                'SELECT * FROM user WHERE login = ? AND password = ?', (username, password))
            user = db_cur.fetchone()
            print(user)
            if user:
                session['user_id'] = user['login']
                return redirect('/profile')
            else:
                return render_template('login.html', error='Invalid username or password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        with first_database('db1.db') as db_cur:
            form_data = request.form
            db_cur.execute('''INSERT INTO user (login, password, ipn, full_name, contacts, photo, passport) VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                form_data['login'], form_data['password'], form_data['ipn'], form_data['full_name'], form_data['contacts'], form_data['photo'], form_data['passport']))
        return redirect('/login')


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    if request.method == 'GET':
        return render_template('logout.html')
    if request.method == 'POST':
        return 'POST'
    else:
        return 'DELETE'


@login_required
@app.route('/profile', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def profile():
    if request.method == 'GET':
        with first_database('db1.db') as db_cur:
           db_cur.execute('SELECT * FROM user WHERE login = ?',
                          (session['user_id'],))
           user = db_cur.fetchone()
           return render_template('profile.html', user=user)
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'DELETE':
        return 'DELETE'


@login_required
@app.route('/profile/favourites', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def profile_fav():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'POST':
        return 'POST'
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/profile/favourites/<favourite_id>', methods=['DELETE'])
def del_fav(favourite_id):
    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/prof-hist', methods=['GET', 'DELETE'])
def prof_hist():
    if request.method == 'GET':
        with first_database('db1.db') as db_cur:
            db_cur.execute('SELECT * FROM search_history')
            history = db_cur.fetchall()
            return render_template('profile.html', history=history)

    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/item', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        with first_database('db1.db') as db_cur:
            db_cur.execute('SELECT * FROM item')
            item = db_cur.fetchall()
            return render_template('item.html', item=item)

    if request.method == 'POST':
       with first_database('db1.db') as db_cur:
           form_data = request.form
           db_cur.execute('''INSERT INTO item (name, photo, description, price_hour, price_day, price_week, price_month) VALUES (:name, :photo, :description, :price_hour, :price_day, :price_week, :price_month)''', request.form)

           return redirect('/item')


@ app.route('/item/<item_id>', methods=['GET', 'DELETE'])
def item(item_id):
    if request.method == 'GET':
        with first_database('db1.db') as db_cur:
            db_cur.execute('SELECT * FROM item')
            item = db_cur.fetchone()
            return render_template('item.html', item=item)
    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/leasers', methods=['GET'])
def leasers():
    if request.method == 'GET':
        return 'GET'


@app.route('/leasers/<leasers_id>', methods=['GET'])
def leaser(leasers_id):
    if request.method == 'GET':
        return 'GET'


@login_required
@app.route('/contract', methods=['GET', 'POST'])
def contracts():
    if request.method == 'GET':
        with first_database('db1.db') as db_cur:
            db_cur.execute('select * from contract')
            contracts = db_cur.fetchall()
            return render_template('contract.html', contracts=contracts)
    if request.method == 'POST':
        with first_database('db1.b') as db_cur:
            form_data = request.form
            db_cur.execute(
                '''INSERT INTO contract (text,start_date,end_date,leaser,taker,item) values (:text,:start_date,:end_date,:leaser,:taker,:item)''', request.form)
            return redirect('/')

@app.route('/contract/<contracts_id>', methods=['GET', 'PATCH', 'PUT'])
def contract(contracts_id):
    if request.methods == 'GET':
        return 'GET'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'PUT':
        return 'PUT'


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.methods == 'GET':
        return 'GET'
    if request.methods == 'POST':
        return 'POST'


@app.route('/complain', methods=['POST'])
def complain():
    if request.method == 'POST':
        with first_database('db1.db') as db_cur:
            form_data = request.form
            db_cur.execute(
                '''INSERT INTO feedback (author,user,grade,contract) VALUES(:author, :user, :grade, :contract)''', request.form)
            return redirect('/')


@app.route('/compare', methods=['GET', 'PUT', 'PATCH'])
def compare():
    if request.methods == 'GET':
        return 'GET'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'PUT':
        return 'PUT'


if __name__ == '__main__':
    app.run(debug=True)  # Imposta debug=True per facilitare il debug
