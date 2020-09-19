import DanceRepertoireMkr
import SpotifyConnect
import pandas as pd
import os

"""
Updates a repertoire of songs based on the Spotify playlist 'Dance Hits'. 
The repertoire consists of the key and bpm of songs in that playlist.
Requires a Spotify developer account.
"""

def updating_rep():
	# Read the csv
	csv1 = pd.read_csv('DanceHitsCollection.csv')
	csv2 = pd.read_csv('Temp.csv')
	og = csv1.values
	og = og[:, 1:]
	new = csv2.values
	new = new[:, 1:]

	# Making a new csv 
	data = []
	for row in og:
	    data.append(row)

	for row_new in new:
	    same = False
	    for row_og in og:
	        if (row_new[0] + row_new[1]) == (row_og[0] + row_og[1]):
	            same = True
	            break
	    if same == False:
	        data.append(row_new)

	data = sorted(data, key=lambda x: x[4])
	columns = ['artist', 'song', 'key', 'mode', 'bpm', 'uri']
	df = pd.DataFrame(data, columns=columns)
	save = df.to_csv('DanceHitsCollection.csv')
	return


if __name__ == "__main__":

	sp = SpotifyConnect.connect()
	print('- Retrieving new songs')
	tracks_id = DanceRepertoireMkr.get_new_songs(sp)
	print('- Making repertoire')
	DanceRepertoireMkr.make_dance_repertoire(sp, tracks_id, 'Temp')
	print('- Updating repertoire')
	updating_rep()
	print('- Removing temporary repertoire')
	os.remove('Temp.csv')
	print('Done!')
	input()

