from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
#from ChordPrediction import test
#from ChordPrediction import model1
#from ChordPrediction import preprocessing
from test import printpred
from pathlib import Path
from playsound import playsound

class MusicMaker(App):


    chord_color_map =  {"C" : [2.55,1.02,1.02, 1],"Db" : [2.55, 1.78, 1.02, 1], "D" :   [2.55, 2.55, 1.02, 1],"Eb" :   [1.78, 2.55, 1.02, 1], "E" :  [1.02, 2.55, 1.02, 1],    "F" :   [1.02, 2.55, 1.78, 1],    "Gb" :   [1.02, 2.55, 2.55, 1],        "G" :   [1.02, 1.78, 2.55, 1],           "Ab" :   [1.02, 1.02, 2.55, 1],            "A" :   [1.78, 1.02, 2.55, 1],  "Bb":[2.55, 1.02, 2.55, 1],           "B":[2.55, 1.02, 1.78, 1],               "Cm":[1.53, 0, 0, 1],            "Dbm":[1.53, .76, 0, 1],           "Dm":[1.53, 1.53, 0, 1],             "Ebm" : [.76, 1.53, 0, 1],           "Em" : [0, 1.53, 0, 1],              "Fm" : [0, 1.53, .76, 1],                 "Gbm":[0, 1.53, 1.53, 1],                     "Gm":[0, .76, 1.53, 1],              "Abm":[.51, .51, 2.55, 1],                 "Am":[.76, 0, 1.53, 1],        "Bbm":[1.53, 0, 1.53, 1],               "Bm":[1.53, 0, .76, 1] }
    #list storing the chord strings in the playlist
    playlist_chords = []
    
    #list storing the playlist buttons
    playlist_buttons = []

    #boolean storing the state of the checkbox
    #default is not demo mode (i.e. selecting chord adds to playlist)
    is_demo = True
    
    #index storing the current number of chords in the playlist
    index = 0

    #list storing the suggestion buttons
    suggestions = []


    def add_to_playlist(self, chord_in):
        if len(self.playlist_chords) <= 7:
            self.playlist_chords.append(chord_in)
            print(self.playlist_chords)
            self.playlist_buttons[self.index].text = chord_in
            self.playlist_buttons[self.index].background_color = self.chord_color_map[chord_in]
            self.index += 1
            #self.playlist_chords[self.index + 1].text = "Hi"
            

    def add_suggestions(self):
        sugg = printpred(self.playlist_chords).keys()
        ind = 0
        for i in sugg:
            if ind <= 3:
                self.suggestions[ind].text = i
                self.suggestions[ind].background_color = self.chord_color_map[i]
                ind += 1
            


    def select_chord(self, instance):
        print(instance.text)
        if self.is_demo:
            playsound('Chord_Resources/' + instance.text + '.wav')
        else:
            if len(instance.text) > 0:   
                self.add_to_playlist(instance.text)
                self.add_suggestions()
        


    def play_playlist(self, chord_in):
        for chord in self.playlist_chords:
            playsound('Chord_Resources/' + chord + '.wav')

    def clear_playlist(self, instance):
        self.index = 0
        self.playlist_chords.clear()
        for but in self.playlist_buttons:
            but.text = ""
            but.background_color = (1, 1, 1, 1)
        for but in self.suggestions:
            but.text = ""
            but.background_color = (1, 1, 1, 1)

    def in_demo_mode(self, instance, is_selected):
        print(instance)
        self.is_demo = is_selected
        print(self.is_demo)


    def build(self):
               
        chord_list = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B',
                        'Cm', 'Dbm', 'Dm', 'Ebm', 'Em', 'Fm', 'Gbm', 'Gm', 'Abm', 'Am', 'Bbm', 'Bm']
        

        #box layout, root of all layouts
        root = BoxLayout(orientation='vertical')

        #grid layout for top half of the screen
        top_grid = GridLayout(cols=3)

        #grid_layout for buttons on side
        button_group = GridLayout(rows=4)

        #start button to start playing playlist
        start = Button(text='START')
        start.bind(on_press=self.play_playlist)
        start.background_color=(1,2.55,1,1)
        button_group.add_widget(start)

        #clear button to clear the playlist
        clear = Button(text='CLEAR')
        clear.bind(on_press=self.clear_playlist)
        clear.background_color=(2.55,1,1,1)
        button_group.add_widget(clear)

        #text box saying "demo mode"
        text = Label(text="Demo \nMode")

        #check box to determine whether or not the app is in 'demo' mode
        checkbox = CheckBox()
        checkbox.active = self.is_demo
        checkbox.bind(active=self.in_demo_mode)
        checkbox.size_hint=(.5, .5)
        checkbox.color = (2.55, 2.55, 2.55, 1)
        button_group.add_widget(text)
        button_group.add_widget(checkbox)
        button_group.size_hint=(.2,.2)


        #grid layout for chord suggestions
        suggestions_layout = GridLayout(rows=2, cols=2)

        for i in range (0, 4):
            temp = Button()
            self.suggestions.append(temp)
            suggestions_layout.add_widget(temp)
            temp.bind(on_press=self.select_chord)


        #grid layout for playlist
        playlist_layout = GridLayout(rows=1)

        #setting up playlist buttons
        for i in range (0, 8):
            temp = Button()
            self.playlist_buttons.append(temp)
            playlist_layout.add_widget(temp)
            
        #grid defining chord keyboard
        bottom_grid = GridLayout(cols=12)

        #list of all buttons in chord keyboard
        buttons = []
        for chord in chord_list:
            temp = Button(text=chord)
            buttons.append(temp)
            temp.background_color=(self.chord_color_map[chord])
            bottom_grid.add_widget(temp)
            temp.bind(on_release=self.select_chord)
        
        top_grid.add_widget(button_group)
        top_grid.add_widget(playlist_layout)
        top_grid.add_widget(suggestions_layout)
        root.add_widget(top_grid)
        root.add_widget(bottom_grid)
        bottom_grid.size_hint=(1, .70)

        return root

if __name__ == '__main__':
    MusicMaker().run()
