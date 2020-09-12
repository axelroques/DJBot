import csv

"""
Gives a list of harmonically compatible songs from a repertoire. 
User inputs the key, only # are accepted. 
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



if __name__ == "__main__":

	again = True

	while again == True:

		with open('Repertoire.csv', newline='') as csvfile:
		    r = csv.reader(csvfile, delimiter=',', quotechar='|')
		    recommendations = []
		    same_key = []
		    harmonic_keys = []
		    minor = False
		    
		    key = input('Enter key: \t')
		    
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
	    
		    for row in r:
		        # Same key
		        if (str(row[3])+str(row[4])) == key:
		            same_key.append(" ".join([row[1], row[2], row[5] + ' bpm', str(row[3])+str(row[4])]))
		        # Harmonic mixing
		        if (((str(row[3])+str(row[4]))) == up_fifth) or \
		        (((str(row[3])+str(row[4]))) == low_fifth) or \
		        (((str(row[3])+str(row[4]))) == major2minor):
		            harmonic_keys.append(" ".join([row[1], row[2], row[5] + ' bpm', str(row[3])+str(row[4])]))

		# Results
		print('\n------------------------------------------------\n')
		print('\t\t\t\t --- SAME KEY ---\n')
		for result in same_key:
			print(result)
		print('\n------------------------------------------------\n')
		print('\t\t\t\t --- HARMONIC MIXING ---\n')
		for result in harmonic_keys:
			print(result)

		print('\n------------------------------------------------\n')
		ans = input('Another key? (y/n) \t')
		if ans == 'n':
			again = False