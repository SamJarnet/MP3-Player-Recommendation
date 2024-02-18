from tkinter import Tk, Listbox, Scrollbar, Text, Button
import numpy as np
import pandas as pd
# import network

class SearchWindow:
    def __init__(self, mp3_player):
        self.mp3_player= mp3_player
     #opens a new window for searching and selecting songs to add
    def openNewWindow(self):
        new_window = Tk()
        new_window.title("New Window")
        new_window.geometry("400x500")
        master = new_window

        #creates window features 
        self.load_box =  Listbox(master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkblue", width=30, height=28)
        self.load_box.place(x=10, y=10)

        self.scrollbar = Scrollbar(master, width=30)
        self.scrollbar.place(x=300, y=100)

        self.load_box.config(yscrollcommand = self.scrollbar.set) 
        self.scrollbar.config(command = self.load_box.yview)

        self.search_box = Text(master, height=1, width=10)
        self.search_box.place(x=200, y=20)

        self.info_box = Listbox(master, height=14, width = 30)
        self.info_box.place(x=200, y=200)

        self.searched_songs = []
       
        self.search_button = Button(master, text="Search", command=self.search_music)
        self.search_button.place(x=300, y=20)

        self.add_song_button= Button(master, text="Add song", command=self.add_song)
        self.add_song_button.place(x=300, y=60)

        self.show_info_button = Button(master, text="Show information", command=self.show_info)
        self.show_info_button.place(x=300, y=100)

        #gets the data from the csv and loads the first 100 songs into the listbox
        self.data = pd.read_csv("data\\data.csv")
        self.data = np.array(self.data).T
        for i in range(0, 100):
            self.load_box.insert(0, self.data[15][i])
            self.searched_songs.insert(0, i)

        self.selected_playlist = self.mp3_player.selected_playlist

    #adds the selected song into the selected playlist and writes it to the file for saving
    def add_song(self):
        self.mp3_player.playlist.insert(0, self.load_box.get(self.load_box.curselection()[0]))
        self.mp3_player.stored_songs[self.selected_playlist].insert(0, self.load_box.get(self.load_box.curselection()[0]))
        with open(self.mp3_player.stored_playlists[self.selected_playlist][0]+ self.mp3_player.login_manager.user +".txt", "w") as file:
            for line in self.mp3_player.stored_songs[self.selected_playlist]:
                file.write("".join(line) + "\n")
        self.add_bias_predictions()                
        self.mp3_player.remove_empty_lines(self.mp3_player.stored_playlists[self.selected_playlist][0]+ self.mp3_player.login_manager.user +".txt")

    #shows the artist and year of release of the selected song
    def show_info(self):
        print(self.searched_songs)
        self.info_box.delete(0, "end")
        artists = self.data[16][self.searched_songs[self.load_box.curselection()[0]]]
        artists = artists.replace("[", "")
        artists = artists.replace("]", "")
        artists = artists.split(",")
        year = str(int(self.data[1][self.searched_songs[self.load_box.curselection()[0]]]*2020))
        for i in range(0, len(artists)):
            self.info_box.insert(i,"Artist: " + artists[i])
        self.info_box.insert(len(artists)+1, "Year: " + year)

    #takes the input from the search box and searches for all songs that contain the inputted text (with some padding)
    def search_music(self):
        text = self.search_box.get(1.0, "end-1c")
        self.load_box.delete(0, "end")
        self.searched_songs = []
        for i in range(0, 100000):
            if self.data[15][i][0:len(text)].lower() == text.lower() or (self.data[15][i].lower().__contains__(text.lower()) and (len(text)-(self.data[15][i].lower().find(text.lower())) )**2 < 25 and len(text) > 2):
                self.searched_songs.insert(0, i)
                self.load_box.insert(0, self.data[15][i])

    def add_bias_predictions(self):
        for i in range(0, 14):
            self.mp3_player.song_count += 1

            self.mp3_player.song_score[self.mp3_player.selected_playlist] += self.data[i][self.searched_songs[self.load_box.curselection()[0]]]
            #result = network.forward_prop(network.W1, network.b1, network.W2, network.b2, network.data_train[i][self.searched_songs[self.load_box.curselection()[0]]])

            # for i in range(0, len(result)):
            #     try:
            #         self.mp3_player.song_score += sum(result[i])
            #     except:
            #         pass