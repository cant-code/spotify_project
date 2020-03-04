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
    clear_data()
    if 'recommendation' not in session:
        session['recommendation'] = []
        session['count'] = 0
    title = 'Homepage'
    return render_template("index.html", title=title)


@app.route('/tracks/')
def display():
    title = 'Tracks'
    if (session.get('limit') != '') is True:
        data = st.get_data(session.get('token'), session.get('username'), session.get('term'),
                           size=session.get('limit'), search_type='Track')
    else:
        data = st.get_data(session.get('token'), session.get('username'), session.get('term'), search_type='Track')
    session['data'] = data
    if data == 404:
        return render_template('error.html', title='Error', error='User Not Found')
    return render_template("display.html", title=title, data=data)


@app.route('/artists/')
def artists():
    title = 'Artists'
    if (session.get('limit') != '') is True:
        data = st.get_data(session.get('token'), session.get('username'), session.get('term'),
                           size=session.get('limit'), search_type='Artist')
    else:
        data = st.get_data(session.get('token'), session.get('username'), session.get('term'), search_type='Artist')
    session['data'] = data
    if data == 404:
        return render_template('error.html', title='Error', error='User Not Found')
    return render_template("artists.html", title=title, data=data)


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
    try:
        returned_value = st.authenticate(session.get("auth").get("oauth"), session.get("code"))
        session['token'] = returned_value
        if session.get('search') == 'tracks':
            return redirect(url_for('display'))
        elif session.get('search') == 'artists':
            return redirect(url_for('artists'))
        else:
            return redirect(url_for('result'))
    except:
        return render_template("error.html", error="Wrong username")


@app.route('/hmm', methods=['POST'])
def hmm():
    song_id = request.values.get('id')
    recom = request.values.get('recom')
    data2 = session.get('data')
    song = None
    if recom == 'true':
        for i in data2[1:]:
            for j in i.get('tracks'):
                if song_id == j.get('id'):
                    song = search_song(j)
        return jsonify(song)
    if session.get('search') == 'tracks':
        for i in data2[1:]:
            for j in i.get('items'):
                if song_id == j.get('id'):
                    song = search_song(j)
        return jsonify(song)
    else:
        for i in data2[1].get('tracks').get('items'):
            if song_id == i.get('id'):
                song = search_song(i)
        return jsonify(song)


@app.route('/foo', methods=['POST'])
def foo():
    artist_id = request.values.get('id')
    data2 = session.get('data')
    artist2 = None
    if session.get('search') == 'artists':
        for i in data2[1:]:
            for j in i.get('items'):
                if artist_id == j.get('id'):
                    artist2 = search_artist(j)
        return jsonify(artist2)
    else:
        for i in data2[1].get('artists').get('items'):
            if artist_id == i.get('id'):
                artist2 = search_artist(i)
        return jsonify(artist2)


@app.route('/alb', methods=['POST'])
def alb():
    playlist_id = request.values.get('id')
    data2 = session.get('data')
    playlist = []
    for j in data2[1].get('playlists').get('items'):
        if playlist_id == j.get('id'):
            playlist.append(j.get('name'))
            playlist.append(j.get('images')[0].get('url'))
            playlist.append(j.get('description'))
            playlist.append(j.get('owner').get('display_name'))
            playlist.append(j.get('external_urls').get('spotify'))
            playlist.append(j.get('tracks').get('total'))
    return jsonify(playlist)


@app.route('/play', methods=['POST'])
def play():
    album_id = request.values.get('id')
    data2 = session.get('data')
    album = []
    artist = []
    for j in data2[1].get('albums').get('items'):
        if album_id == j.get('id'):
            album.append(j.get('name'))
            album.append(j.get('images')[0].get('url'))
            for k in j.get('artists'):
                artist.append(k.get('name'))
            album.append(artist)
            album.append(j.get('total_tracks'))
            album.append(j.get('external_urls').get('spotify'))
            album.append(j.get('release_date'))
    return jsonify(album)


@app.route('/search', methods=['POST', 'GET'])
def search():
    title = 'Search Page'
    if 'recommendation' not in session:
        session['recommendation'] = []
        session['count'] = 0
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['criteria'] = request.form.getlist('criteria')
        session['query'] = request.form['query']
        if request.form['limit'] == '':
            limit = 5
        else:
            limit = request.form['limit']
        session['limit'] = limit
        new_data = st.get_token(request.form['username'])
        if "access_token" in new_data:
            session['token'] = {'token': new_data['access_token']}
            return redirect(url_for('result'))
        else:
            session['auth'] = new_data
            return redirect(session.get("auth").get("auth_url"))
    return render_template("search.html", title=title)


@app.route('/results')
def result():
    title = 'Search Results'
    data = st.search(session.get('token'), session.get('username'), session.get('query'), session.get('limit'),
                     session.get('criteria'))
    if data == 404:
        return render_template('error.html', title='Error', error='User Not Found')
    session['data'] = data
    return render_template("search_result.html", title=title, data=data)


@app.route('/list')
def recom_list():
    if 'recom' not in session:
        session['recom']= 'true'
    data_id = request.values.get('id')
    data_type = request.values.get('type')
    query = request.values.get('query')
    if query == 'add':
        if session['count'] < 5:
            for i in session['recommendation']:
                if i.get('d_id') == data_id:
                    return jsonify(404)
            src = request.values.get('src')
            name = request.values.get('name')
            data = {'d_id': data_id, 'd_src': src, 'd_name': name, 'type': data_type}
            session['count'] += 1
            session['recommendation'].append(data)
            return jsonify({'success': True})
        else:
            return jsonify(404)
    else:
        for i in session['recommendation']:
            if i.get('d_id') == data_id:
                session['recommendation'].remove(i)
                session['count'] -= 1
                return jsonify({'success': True})


@app.route('/data')
def data():
    return jsonify(session['recommendation'])


@app.route('/getrecom')
def get_recom():
    title = 'Recommendations'
    limit = request.values.get('limit')
    if limit is None:
        limit = 5
    data = st.recommendations(session.get('token'), session.get('username'), session.get('recommendation'), limit)
    if data == 404:
        return render_template('error.html', title='Error', error='User Not Found')
    session['data'] = data
    del session['recommendation']
    del session['recom']
    if 'recommendation' not in session:
        session['recommendation'] = []
        session['count'] = 0
    return render_template("recresults.html", title=title, data=data)


if __name__ == '__main__':
    app.run()


def clear_data():
    if 'limit' in session:
        del session['limit']
    if 'term' in session:
        del session['term']
    if 'data' in session:
        del session['data']
    if 'criteria' in session:
        del session['criteria']
    if 'query' in session:
        del session['query']
    if 'search' in session:
        del session['search']


def search_artist(j):
    artist2 = [j.get('name'), j.get('images')[0].get('url'), j.get('popularity'), j.get('followers').get('total'),
               j.get('external_urls').get('spotify')]
    return artist2


def search_song(j):
    song = []
    artist = []
    song.append(j.get('name'))
    song.append(j.get('album').get('images')[0].get('url'))
    for k in j.get('artists'):
        artist.append(k.get('name'))
    song.append(artist)
    song.append(j.get('duration_ms'))
    song.append(j.get('external_urls').get('spotify'))
    return song
