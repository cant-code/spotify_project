from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import spotify_test as st
from datetime import timedelta
from flask_session import Session
import os

app = Flask(__name__)
app.config['SECRET-KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)


@app.route('/')
def hello_world():
    session.permanent = True
    title = 'Homepage'
    return render_template("index.html", title=title)


@app.route('/tracks/')
def display():
    title = 'Tracks'
    if (session.get('limit') != '') is True:
        data = st.get_data(session.get('token'), session.get('username'), session.get('term'),
                           size=session.get('limit'))
    else:
        data = st.get_data(session.get('token'), session.get('username'), session.get('term'))
    if 'limit' in session:
        del session['limit']
    del session['token']
    if data is None:
        return "Empty"
    return render_template("display.html", data=data)


@app.route('/artists/')
def artists():
    title = 'Artists'
    if (session.get('limit') != '') is True:
        data = st.get_artists(session.get('token'), session.get('username'), session.get('term'),
                              size=session.get('limit'))
    else:
        data = st.get_artists(session.get('token'), session.get('username'), session.get('term'))
    if 'limit' in session:
        del session['limit']
    del session['token']
    if data is None:
        return "Empty"
    return render_template("artists.html", data=data)


@app.route('/', methods=['POST'])
def get_username():
    data = request.form['username']
    term = request.form['term']
    limit = request.form['limit']
    session['search'] = request.form['search']
    session['username'] = data
    session['term'] = term
    if (limit != '') is True:
        session['limit'] = limit
    new_data = st.get_token(data)
    if "access_token" in new_data:
        session['token'] = {'token': new_data['access_token']}
        if request.form['search'] == 'tracks':
            return redirect(url_for('display'))
        else:
            return redirect(url_for('artists'))
    else:
        session['auth'] = new_data
        return redirect(session.get("auth").get("auth_url"))


@app.route('/auth/')
def auth():
    session['code'] = str(request.url)
    returned_value = st.authenticate(session.get("auth").get("oauth"), session.get("code"))
    session['token'] = returned_value
    if session.get('search') == 'tracks':
        return redirect(url_for('display'))
    else:
        return redirect(url_for('artists'))


if __name__ == '__main__':
    app.run()
