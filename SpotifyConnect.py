from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

def connect():

	cid = ''
	secret = ''

	try:
		client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
		sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
		print('- Connected to Spotify')
	except:
		print("- Can't connect to Spotify")
		input()

	return sp