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
    if 'limit' in session:
        del session['limit']
    if 'username' in session:
        del session['username']
    if 'term' in session:
        del session['term']
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
    session['data'] = data
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


@app.route('/hmm', methods=['POST'])
def hmm():
    song_id = request.values.get('id')
    data2 = session.get('data')
    song = []
    artist = []
    for i in data2[1:]:
        for j in i.get('items'):
            if song_id == j.get('id'):
                song.append(j.get('name'))
                song.append(j.get('album').get('images')[0].get('url'))
                for k in j.get('artists'):
                    artist.append(k.get('name'))
                song.append(artist)
                song.append(j.get('duration_ms'))
                song.append(j.get('external_urls').get('spotify'))
    return jsonify(song)


if __name__ == '__main__':
    app.run()
