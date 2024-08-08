from flask import Flask, render_template, abort, request, make_response, redirect, url_for
import data

app = Flask(__name__)

users = {
    'admin1': 'admin1',
    'admin2': 'admin2'
}


@app.route('/add_tour/')
def add_tour():
    return render_template('form.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            return render_template('register.html', error='User already exists')
        users[username] = password
        res = make_response(redirect(url_for('main')))
        res.set_cookie('username', username, max_age=60*60*24*365*2)
        return res
    return render_template('register.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            res = make_response(redirect(url_for('main')))
            res.set_cookie('username', username, max_age=60*60*24*365*2)
            return res
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout/')
def logout():
    res = make_response(redirect(url_for('login')))
    res.set_cookie('username', '', expires=0)
    return res

@app.route('/cookie/')
def cookie():
    if not request.cookies.get('username') or request.cookies.get('username') == 'None':
        return redirect('/login/')
    else:
        res = make_response(f"Value of cookie is {request.cookies.get('username')}")
        return res

# @app.route('/agent/')
# def agent():
#     user_agent = request.headers.get('User-Agent')
#     return f'<b>Your browser is {user_agent}</b>'

@app.route('/main/')
@app.route('/')
def main():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login'))
    return render_template('index.html', departures=data.departures, title=data.title, subtitle=data.subtitle, description=data.description, tours=data.tours, cookie=username)

@app.route('/tour/<int:id>/')
def tour(id):
    return render_template('tour.html', tour=data.tours[id], title=data.title, departures=data.departures)

@app.route('/departures/')
def departure_zero():
    return render_template('index.html', departures=data.departures, title=data.title, subtitle=data.subtitle, description=data.description, tours=data.tours)


@app.route('/departures/<departure>/')
def departure(departure):
    if departure not in data.departures:
        abort(404)

    tours = dict(filter(lambda tour: tour[1]["departure"].lower() == departure.lower(), data.tours.items()))
    if tours:
        return render_template('departure.html', departure=departure, title=data.title, departures=data.departures,
                               tours=tours)
    abort(404)

@app.route('/dosearch/', methods=['GET'])
def dosearch():
    query = request.args.get('s', '').lower()
    results = {id: tour for id, tour in data.tours.items() if query in tour['title'].lower() or query in tour['description'].lower()}
    return render_template('search_results.html', query=query, results=results)

@app.route('/buy_tour', methods=['GET', 'POST'])
def buy_tour():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        tour_id = request.form['tour_id']
        return redirect(url_for('confirmation'))
    return render_template('buy_tour.html')

@app.route('/confirmation')
def confirmation():
    return render_template('success.html')




if __name__ == '__main__':
    app.run(debug=True)



