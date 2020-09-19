import SpotifyConnect
import pandas as pd
import spotipy
import math
import os

"""
Makes a repertoire of songs based on the Spotify playlist 'Dance Hits'. 
The repertoire consists of the key and bpm of songs in that playlist.
Requires a Spotify developer account.
"""

key_dict = {
    0:'C',
    1:'C#',
    2:'D',
    3:'D#',
    4:'E',
    5:'F',
    6:'F#',
    7:'G',
    8:'G#',
    9:'A',
    10:'A#',
    11:'B'
    }

mode_dict = {
    0:'m',
    1:''
    }


def get_new_songs(sp):
	# Search for that playlist
	results = sp.search(q='Dance Hits', type='playlist', limit=1)
	results = results['playlists']['items'][0]
	name = results['name']
	uri = results['uri']

	# Get the ids from the songs in that playlist
	playlist_id = uri
	offset = 0
	tracks_id = []
	while True:
	    response = sp.playlist_items(playlist_id,
	                                 offset = offset,
	                                 fields = 'items.track.id,total',
	                                 additional_types = ['track'])
	    
	    # Response is limited to 100 outputs everytime so we have to iterate if 
	    # there are more than 100 songs in the playlist 
	    offset = offset + len(response['items'])
	    #print(offset, "/", response['total'])
	    
	    for track in response['items']:
	        tracks_id.append(track['track']['id'])

	    if len(response['items']) == 0:
	        break
	return tracks_id


def make_dance_repertoire(sp, tracks_id, rep_name):
	# Make the repertoire
	songs_artist = []
	songs_name = []
	songs_key = []
	songs_mode = []
	songs_bpm = []
	songs_uri = []

	for ids in tracks_id:
	    result = sp.track(ids)
	    try:
	        uri = result['uri']
	        features = sp.audio_features(tracks=[uri])[0]
	        
	        artist = result['artists'][0]['name']
	        artist = artist.replace(',', '')
	        songs_artist.append(artist)
	        
	        name = result['name']
	        name = name.replace(',', '')
	        songs_name.append(name)
	        
	        songs_key.append(key_dict[features['key']])
	        songs_mode.append(mode_dict[features['mode']])
	        songs_bpm.append(math.ceil(features['tempo']))
	        songs_uri.append(uri)
	    except:
	        pass

	all_songs = pd.DataFrame({
	    'artist':songs_artist,
	    'song':songs_name,
	    'key':songs_key,
	    'mode':songs_mode,
	    'bpm':songs_bpm,
	    'uri':songs_uri
	    })

	data = all_songs.values
	data = sorted(data, key=lambda x: x[4])
	columns = ['artist', 'song', 'key', 'mode', 'bpm', 'uri']
	df = pd.DataFrame(data, columns=columns)
	save = df.to_csv(rep_name + '.csv')
	return



if __name__ == "__main__":

	sp = SpotifyConnect.connect()
	print('- Retrieving new songs')
	tracks_id = get_new_songs(sp)
	print('- Making repertoire')
	make_dance_repertoire(sp, tracks_id, 'Repertoire_DanceHits')	
	print('Done!')
	input()