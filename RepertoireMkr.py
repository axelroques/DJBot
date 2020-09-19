import SpotifyConnect
import pandas as pd
import spotipy
import math
import os

"""
Makes a repertoire of songs based on an existing music folder. 
The repertoire consists of the key and bpm of songs that were able to be identified with 
the Spotify API based on their names.
Requires a Spotify developer account and a folder with .mp3 files.
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


def clean_name(file):
    # File name cleaning
    file = file.replace('.mp3', '')
    file = file.replace(' -', '')
    file = file.replace(',', '')
    file = file.replace('OG', '')
    file = file.replace('(Explicit)', '')
    file = file.split('[')[0]
    file = file.split('HQ')[0]
    file = file.split('Official')[0]
    file = file.split('Remix')
    try:
        test = file[1]
        file = file[0].replace('(', '')
    except:
        file = file[0].split('(')[0]
    return file




if __name__ == "__main__":

	sp = SpotifyConnect.connect()
	
	path = ''

	songs_artist = []
	songs_name = []
	songs_key = []
	songs_mode = []
	songs_bpm = []
	songs_uri = []

	print("- Starting analysis of songs in", path)
	for _, _, files in os.walk(path):
	    for file in files:
	        file = clean_name(file)
	        result = sp.search(q=file, limit=5)
	        try:
	            uri = result['tracks']['items'][0]['uri']
	            features = sp.audio_features(tracks=[uri])[0]
	            artist = result['tracks']['items'][0]['artists'][0]['name']
	            artist = artist.replace(',', '')
	            songs_artist.append(artist)
	            name = result['tracks']['items'][0]['name']
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

	save = df.to_csv('Repertoire.csv')
	print('- Repertoire created!')
	input()