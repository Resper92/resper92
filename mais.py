from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
from sqlalchemy import select, delete
from functools import wraps
from conectdb import init_db, db_session
from model import User, Item, Contract, Favorite, Feedback, Search_history
import celery_worker

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

# class first_database():
#     def __init__(self, file_name):
#         self.con = sqlite3.connect(file_name)
#         self.con.row_factory = dict_factory
#         self.cur = self.con.cursor()

#     def __enter__(self):
#         return self.cur

#     def __exit__(self, type, value, traceback):
#         self.con.commit()
#         self.con.close()



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

        init_db()
        user_data = db_session.execute(
            select(User).filter_by(login=username, password=password)
        ).scalar()
        if user_data:
            session['user'] = user_data.user_id
            return redirect('/profile')
        else:
            return render_template('login.html', error='Invalid username or password')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        form_data = dict(request.form)
        init_db()
        user = User(**form_data)
        db_session.add(user)
        db_session.commit()
        return redirect('/login')


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    session.pop('user', None)
    return redirect('/login')

@login_required
@app.route('/profile', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def profile():
    init_db()
    if session.get('user') is None:
        return redirect('/login')
    if request.method == 'GET':
        user_data = db_session.execute(
            select(User).filter_by(user_id=session['user'])).scalar()
        return render_template('profile.html', user=user_data)
    if request.method == 'PUT':
      user = db_session.execute(select(user).filter_by(
          user_id=session['user'])).scalar()
      user.full_name = request.form['full_name']
      db_session.commit()
      return redirect('/profile')
    if request.method == 'DELETE':
        user = db_session.execute(select('user').filter_by(
            user_id=session['user'])).scalar()
        db_session.delete(user)
        db_session.commit()
        session.pop('user', None)
        session.pop(login, None)
        return redirect('/login')



@login_required
@app.route('/favorite', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def fav():
    if request.method == 'GET':
        init_db()
        fav_id_items = db_session.execute(
            select(Favorite.item).filter_by(user=session['user'])).scalars().all()

        fav_it = db_session.execute(
            select(Item).filter(Item.id.in_(fav_id_items))).scalars().all()

        return render_template('favorite.html', fav=fav_it)

    if request.method == 'POST':
        init_db()
        item = request.form.get('item_id')
        user = session.get('user')
        fav = Favorite(user=user, item=item)
        db_session.add(fav)
        db_session.commit()

        return redirect('/favorite')



@app.route('/profile/favourites/<favourite_id>', methods=['DELETE'])
def del_fav(favourite_id):
    if request.method == 'DELETE':
        return 'DELETE'


@login_required
@app.route('/prof-hist', methods=['GET', 'DELETE'])
def prof_hist():
    if request.method == 'GET':
       init_db()
       history = db_session.execute(select(Search_history)).scalars()
       return render_template('profile.html', prof_hist=history)

    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/item', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
       init_db()
       item_data = select(Item)
       item_data = db_session.execute(select(Item)).scalars()
       return render_template('item.html', items=item_data)


    if request.method == 'POST':
       if session.get('user') is None:
           return redirect('/login')

       init_db()
       item = Item(**request.form)
       item.owner = session['user']

       db_session.add(item)
       db_session.commit()

       return redirect('/item')


@ login_required
@ app.route('/item/<int:item_id>', methods=['GET', 'DELETE'])
def item(item_id):
    if request.method == 'GET':
        if session.get('user') is None:
            return redirect('/login')
        init_db()
        item = db_session.execute(select(Item).filter_by(id=item_id)).scalar()
        return render_template('item_det.html', item=item, user_id=session['user'])


@ login_required
@ app.route('/item/<int:item_id>/del', methods=['POST'])
def item_del(item_id):
    init_db()
    item = db_session.get(Item, item_id)
    if item and session.get('user') == item.owner:
        db_session.delete(item)
        db_session.commit()
        return render_template("/"), 200
    return jsonify({"error": "Non autorizzato o elemento non trovato"}), 403


@app.route('/leaser', methods=['GET'])
def leasers():
    if request.method == 'GET':
        init_db()
        leasers = db_session.execute(select(User)).scalars()
        return render_template('leaser.html', leasers=leasers)


@app.route('/leasers/<leasers_id>', methods=['GET'])
def leaser(leasers_id):
    if request.method == 'GET':
        init_db()
        leasers_id = db_session.execute(
            select(User).filter_by(user_id=leasers_id)).scalar()
        return 'GET'


@login_required
@app.route('/contract', methods=['GET', 'POST'])
def contract():
    if request.method == 'GET':
        init_db()
        contracts = db_session.execute(select(Contract)).scalars().all()
        leas = db_session.execute(select(User).filter_by(
            user_id=Contract.leaser)).scalar()
        take = db_session.execute(select(User).filter_by(
            user_id=Contract.taker)).scalar()
        it = db_session.execute(select(Item).filter_by(
            id=Contract.item)).scalar()
        return render_template('contract.html', contracts=contracts, leas=leas, take=take, it=it)

    if request.method == 'POST':

        contract = Contract(**request.form)
        contract.leaser = session['user']
        db_session.add(contract)
        db_session.commit()
        celery_worker.send_email(Contract.contract)
        return redirect('/')


@login_required
@app.route('/contract/<int:contract>', methods=['GET', 'PATCH', 'PUT'])
def view_contract(contract):
    if request.method == 'GET':
        init_db()
        if session.get('user') is None:
            return redirect('/login')
        contract = db_session.execute(
            select(Contract).filter_by(contract=contract)).scalar()
        name = db_session.execute(select(User).filter_by(
            user_id=contract.leaser)).scalar()
        name_2 = db_session.execute(select(User).filter_by(
            user_id=contract.taker)).scalar()
        item = db_session.execute(select(Item).filter_by(
            id=contract.item)).scalar()
        print(f"User ID: {session['user']}")
        print(f"Contract Leaser ID: {contract.leaser}")
        print(f"Contract Taker ID: {contract.taker}")
        return render_template('contract_det.html', contract=contract, name=name, name_2=name_2, item=item)
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'PUT':
        return 'PUT'


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        name = request.args.get('name')
        init_db()
        item = db_session.execute(select(Item).filter_by(name=name)).scalar()
        return render_template('item_det.html', item=item)
    if request.methods == 'POST':
        search = Search_history(**request.form)
        search.user = session['user']
        db_session.add(search)
        db_session.commit()
        return 'POST'


@app.route('/complain', methods=['POST'])
def complain():
    if request.method == 'POST':
        init_db()
        complain = Feedback(**request.form)
        db_session.add(complain)
        db_session.commit()
        return redirect('/')


@app.route('/compare', methods=['GET', 'PUT', 'PATCH'])
def compare():
    if request.method == 'GET':
        init_db()
        name1 = db_session.execute(select(Item).filter_by(
            name=request.args.get('name1'))).scalar()
        name2 = db_session.execute(select(Item).filter_by(
            name=request.args.get('name2'))).scalar()
        return render_template('compare.html', item=name1, item2=name2)

    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'PUT':
        return 'PUT'


@app.route('/add_task', methods=['get'])
def set_task():
    celery_worker.add.delay(1, 2)
    return 'task sent'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
