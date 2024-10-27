from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        return 'POST'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration.html')
    if request.method == 'POST':
        return 'POST'


@app.route('/logout', methods=['GET', 'POST', 'DELETE'])
def logout():
    if request.method == 'GET':
        return render_template('logout.html')
    if request.method == 'POST':
        return 'POST'
    else:
        return 'DELETE'


@app.route('/profile', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def profile():
    if request.method == 'POST':
        return 'POST'
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == 'DELETE':
        return 'DELETE'


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


@app.route('/profile/history', methods=['GET', 'DELETE'])
def prof_hist():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'POST':
        return 'POST'


@app.route('/items/<item_id>', methods=['GET', 'DELETE'])
def item(item_id):
    if request.method == 'GET':
        return 'GET'
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


@app.route('/contracts', methods=['GET', 'POST'])
def contracts():
    if request.methods == 'GET':
        return 'GET'
    if request.methods == 'POST':
        return 'POST'


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
        return 'POST'


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
