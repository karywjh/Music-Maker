import Song
import pickle
from music21 import *

valid_tonics = ['C', 'C-', 'C#', 'D', 'D-', 'D#', 'E', 'E-', 'F', 'F#', 'G', 'G-', 'G#', 'A', 'A-', 'A#', 'B', 'B-', 'Cm', 'C-m', 'C#m', 'Dm', 'D-m', 'D#m', 'Em', 'E-m', 'Fm', 'F#m', 'Gm', 'G-m', 'G#m', 'Am', 'A-m', 'A#m', 'Bm', 'B-m']

# Load all songs
with open ("Data/songs.data", "rb") as fil:
    songs = pickle.load(fil)

'''
Get all songs that are in the targeted keys
'''
# def get_songs_in_key(key, song_list):
#     ret = []
#     for song in song_list:
#         if (song.tonic not in valid_tonics):
#             raise NameException('{0} is not a valid tonic'.format(song.tonic))
#         if song.tonic == key:
#             ret.append(song)
#     return ret

'''
Parse the song according to the desired key and chord
'''
def parse(this_chord):
    total_chord_dict = {}
    for song in songs:
        # Parse each song
        this_dict = parse_song(song.chord_list, this_chord)
        # Add this song's dictionary to the total dictionary
        total_chord_dict = addDict(total_chord_dict, this_dict)
    if total_chord_dict == {}:
        return str(total_chord_dict) + "\nThis chord does not appeared in our dataset\nTry a different Chord"
    # Sort the dictionary according to its value
    sorted_dict = dict(sorted(total_chord_dict.items(), key=lambda x: x[1], reverse= True))
    # Turn the value from the occurance to the probability in percentage    
    return calc_probability(sorted_dict, this_chord.figure)


'''
Given the chord list of the song and the targeted chord
Return a dictionary that records every possible "next chord" and their occurances
'''
def parse_song(chord_list, this_chord):
    dictionary = {}
    # Loop through each chord in the list
    for index in range (len(chord_list) - 1):
        # Find the "next chords" of the targeted chord
        if chord_list[index] == this_chord:
            next_chord = chord_list[index + 1]
            # Eliminate any diminished or augmented options
            if next_chord.chordKind == 'major' or 'minor':
                # Key is the String representing the chord
                # Value is an int of the occurance
                if next_chord.figure not in dictionary:
                    dictionary[str(next_chord.root())[:-1].replace('-','b')] = 1
                else:
                    dictionary[str(next_chord.root())[:-1]] += 1
    return dictionary        

'''
    Add two dictionaries together such that the value of the same key adds up
'''
def addDict(dict1, dict2):
    for this_chord in dict2:
        if this_chord not in dict1:
            dict1[this_chord] = dict2[this_chord]
        else:
            dict1[this_chord] += dict2[this_chord]
    return dict1

'''
    Turn the dictionary that has values as the occurance to values as probabilities of occurance
'''
def calc_probability(dictionary, this_chord_name):
    # The sum of all values
    total = 0
    # Filter out the possibility that next chord is the same chord as the targeted chord
    if (this_chord_name in dictionary):
        del dictionary[this_chord_name]
    # Calculate total
    for chord in dictionary:
        total += dictionary[chord]
    # Turn value into percentage
    for chord in dictionary:
        dictionary[chord] = int(dictionary[chord] * 1000 / total) / 1000
    return dictionary

# Test
# p = harmony.ChordSymbol('E')
# q = harmony.ChordSymbol('F')
# print(p.chordKind)
# print(parse(p))
# print(parse(q))