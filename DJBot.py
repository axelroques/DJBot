import SpotifyConnect
import math
import csv
import os

"""
Gives a list of harmonically compatible songs from a repertoire,
or from the Spotify 'Dance Hits' playlist. 
User inputs the name of the song or the key, only # are accepted. 
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

relative_minor = {
    'C':'Am',
    'C#':'A#m',
    'D':'Bm',
    'D#':'Cm',
    'E':'C#m',
    'F':'Dm',
    'F#':'D#m',
    'G':'Em',
    'G#':'Fm',
    'A':'F#m',
    'A#':'Gm',
    'B':'G#m'
    }


def search_repertoire(rep_name, key):
	with open(rep_name + '.csv', newline='') as csvfile:
		r = csv.reader(csvfile, delimiter=',', quotechar='|')
		same_key = []
		harmonic_keys = []
		minor = False

		if 'm' in key:
		    minor = True
		    major2minor = list(relative_minor.keys())[list(relative_minor.values()).index(key)]
		else:
		    major2minor = relative_minor[key]

		key = key.split('m')[0]
		pitch_class = list(key_dict.keys())[list(key_dict.values()).index(key)]
		up_fifth = key_dict[(int(pitch_class)+7)%12]
		low_fifth = key_dict[(int(pitch_class)-7)%12]
		if minor:
		    up_fifth += 'm'
		    low_fifth += 'm'
		    key += 'm'

		for row in r:
		    # Same key
		    if (str(row[3])+str(row[4])) == key:
		        same_key.append(" ".join([row[1], '-', row[2], row[5] + 'bpm', str(row[3])+str(row[4])]))
		    # Harmonic mixing
		    if (((str(row[3])+str(row[4]))) == up_fifth) or \
		    (((str(row[3])+str(row[4]))) == low_fifth) or \
		    (((str(row[3])+str(row[4]))) == major2minor):
		        harmonic_keys.append(" ".join([row[1], '-', row[2], row[5] + 'bpm', str(row[3])+str(row[4])]))

	return same_key, harmonic_keys


def print_results(same_key, harmonic_keys):
	# Results
	print('\n------------------------------------------------\n')
	print('\t\t\t\t --- SAME KEY ---\n')
	for result in same_key:
		print(result)
	print('\n------------------------------------------------\n')
	print('\t\t\t\t --- HARMONIC MIXING ---\n')
	for result in harmonic_keys:
		print(result)
	return





if __name__ == "__main__":

	again = True

	# Main loop
	while again == True:

		fail = True
		# Search song or search by key
		while fail == True:
			ans = input('Search by song or search by key? (s,k) \t')
			if ans not in 'sk':
				print('Command not understood')
			else:
				fail = False

		if ans == 'k':
			key = input('Enter key: \t')
			print('\n------------------------------------------------\n')
			print('Recommendations from the Dance Hit playlist')
			same_key, harmonic_keys = search_repertoire('DanceHitsCollection', key)
			print_results(same_key, harmonic_keys)
			print('\n------------------------------------------------\n')
			print('Recommendations from the repertoire')
			same_key, harmonic_keys = search_repertoire('Repertoire', key)
			print_results(same_key, harmonic_keys)

		elif ans == 's':
			sp = SpotifyConnect.connect()
			song_name = input('Song to search: \t')
			result = sp.search(q=song_name, limit=1)
			try:
				uri = result['tracks']['items'][0]['uri']
				features = sp.audio_features(tracks=[uri])[0]
				artist = result['tracks']['items'][0]['artists'][0]['name']
				name = result['tracks']['items'][0]['name']
				key = key_dict[features['key']] + mode_dict[features['mode']]
				bpm = math.ceil(features['tempo'])
				print('\n------------------------------------------------\n')
				print('Found:\n\t', artist, '-', name, 'in', key, bpm, 'bpm')
				print('\n------------------------------------------------\n')
				print('Recommendations from the Dance Hit playlist')
				same_key, harmonic_keys = search_repertoire('DanceHitsCollection', key)
				print_results(same_key, harmonic_keys)
				print('\n------------------------------------------------\n')
				print('Recommendations from the repertoire')
				same_key, harmonic_keys = search_repertoire('Repertoire', key)
				print_results(same_key, harmonic_keys)

			except:
				print('Song not found')
				break

		print('\n------------------------------------------------\n')
		ans = input('Anything else? (y/n) \t')
		if ans == 'n':
			again = False
		os.system('cls')