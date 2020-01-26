import spotipy
import spotipy.oauth2 as oauth2
import os

spotipy_client_id = os.environ.get('spotipy_client_id')
spotipy_client_secret = os.environ.get('spotipy_client_secret')
spotipy_redirect_uri = os.environ.get('spotipy_redirect_uri')


def get_token(user):
    username = user
    scope = 'user-top-read'
    print(os.environ.get('spotipy_client_secret'))
    print(spotipy_client_id)
    print(spotipy_client_secret)
    print(spotipy_redirect_uri)
    token = prompt_for_user_token(username, scope, client_id=spotipy_client_id,
                                  client_secret=spotipy_client_secret,
                                  redirect_uri=spotipy_redirect_uri)
    return token


def get_data(token, username, term, size):
    if token:
        token2 = token['token']
        sp = spotipy.Spotify(auth=token2)
        sp.trace = False
        result = []
        results2 = sp.user(username)
        result.append(results2)
        if size is None:
            size = 5
        results = sp.current_user_top_tracks(time_range=term, limit=size)
        result.append(results)
        return result
    else:
        return None


def prompt_for_user_token(username, scope=None, client_id=None,
                          client_secret=None, redirect_uri=None,
                          cache_path=None):
    cache_path = cache_path or ".cache-" + username
    sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri,
                                   scope=scope, cache_path=cache_path)
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        data = {
            "oauth": sp_oauth,
            "auth_url": auth_url
        }
        return data
    else:
        return token_info


def authenticate(sp_oauth, response):
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)
    if token_info:
        return {"token": token_info['access_token']}
    else:
        return None


def get_artists(token, username, term, size):
    token2 = token['token']
    sp = spotipy.Spotify(auth=token2)
    sp.trace = False
    result = []
    results2 = sp.user(username)
    result.append(results2)
    if size is None:
        size = 5
    results = sp.current_user_top_artists(time_range=term, limit=size)
    result.append(results)
    return result
