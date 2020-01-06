#object with:
#1. song title
#2. song artist
#3. metre
#4. tonic
#5. list of music21 Harmony objects representing chords in the song

class song:
	def __init__(self, title, artist, metre, tonic, chordList):
		self.title = title
		self.artist = artist
		self.metre = metre
		self.tonic = tonic
		self.chord_list = chordList
		self.set_quality_tonic()

	#takes a Song object as an input and checks whether the tonic is major or minor
	#by looking at every instance of the tonic chord which appears in the song
	#and checking whether on average there are more occurences of the minor or the major
	#then adds "m" to the tonic if minor and adds nothing if major
	def set_quality_tonic(self):
		num_maj = 0
		num_min = 0
		for chord in self.chord_list:
			#get the root of the chord and remove the octave number
			root = str(chord.root())[:-1]
			if root == self.tonic:
				chord_str = chord.findFigure()
				#if the chord is not a simple major chord and the second letter of the chord string
				#is 'm' then it is a major chord so increment nummin
				if len(chord_str) != 1 and chord_str[1] == 'm':          
					num_min += 1
				#otherwise the chord is a major chord so increment num_maj
				else:
					num_maj += 1
		#if there are more minor than major chords, add 'm' to the tonic
		#otherwise leave as is since it is a major chord
		if num_min > num_maj:
			self.tonic += 'm'


valid_tonics = ['C', 'C-', 'C#', 'D', 'D-', 'D#', 'E', 'E-', 'F', 'F#', 'G', 'G-', 'G#', 'A', 'A-', 'A#', 'B', 'B-',
                'Cm', 'C-m', 'C#m', 'Dm', 'D-m', 'D#m', 'Em', 'E-m', 'Fm', 'F#m', 'Gm', 'G-m', 'G#m', 'Am', 'A-m', 'A#m', 'Bm', 'B-m']


def get_songs_in_key(key, song_list):
    ret = []
    for song in song_list:
        if (song.tonic not in valid_tonics):
            raise NameException('{0} is not a valid tonic'.format(song.tonic))
        if song.tonic == key:
            ret.append(song)
    return ret




        
