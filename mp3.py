import os
import pygame
from tkinter import Tk, Frame, Button, Label, Scale, Listbox, StringVar, PhotoImage, Text, Toplevel, Scrollbar
from tkinter import filedialog
from mutagen.mp3 import MP3
import random
import datetime
import numpy as np
import pandas as pd

#import network


class MP3Player:
    def __init__(self, master):


        #initialise the window with its name and geometry
        self.master = master
        self.master.title("MP3 Player")
        self.master.geometry("1280x720")




        #creates and positions the button that is used to create a playlist
        self.create_playlist_button = Button(self.master, text="Create Playlist", command=self.create_playlist)
        self.create_playlist_button.place(x=60, y=65)


        #creates the button that is used to delete a playlist
        self.delete_playlist_button = Button(self.master, text="Delete Playlist", command=self.delete_playlist)
        self.delete_playlist_button.place(x=150, y=65)


        #creates and positions the label for the word "playlists"
        self.playlist_label = Label(self.master, text="Playlists")
        self.playlist_label.place(x=118, y=30)


        #creates and positions the listbox for the playlists
        self.playlist_folder = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=30, height=28)
        self.playlist_folder.place(x=50, y=132)


        #creates and positions the textbox for user input to name their playlists
        self.input_text = Text(height = 1, width = 22)
        self.input_text.place(x=52, y=100)


        #creates and positions the listbox for the selected playlist
        self.playlist = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=90, height=30)
        self.playlist.place(x=300, y=100)


        #creates and positions the label for the title of the selected playlist
        self.playlist_label = Label(self.master, text="No playlist selected")
        self.playlist_label.place(x=300, y=65)
   
        #creates and positions the label for the word "recommended"
        self.recommended_label = Label(self.master, text="Recommended")
        self.recommended_label.place(x=900, y=230)


        #creates and positions the listbox for the recommended section
        self.recommended = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=55, height=20)
        self.recommended.place(x=900, y=260)


        #creates and positions the button to generate recommended songs
        self.generate_button = Button(self.master, text="Generate Songs", command=self.recommend_songs)
        self.generate_button.place(x=1140, y=225)


        #creates and positions the button to add the selected song
        self.add_song_button = Button(self.master, text="Add song", command=self.add_selected_song)
        self.add_song_button.place(x=1060, y=225)


        #creates and positions the button to load a song from files into the selected playlist
        self.load_button = Button(self.master, text="Load Song", command=self.load_song)
        self.load_button.place(x=300, y=27)


        #i forgot what this is for
        self.load_window = Button(self.master, text="Load Window", command=self.openNewWindow)
        self.load_window.place(x=380, y=27)


        #creates and positions the button to delete a song from the playlist
        self.delete_song_button = Button(self.master, text="Delete Song", command=self.delete_song)
        self.delete_song_button.place(x=480, y=27)

        

        #creates and positions the label for the currently playing song
        self.currently_playing_song = Label(self.master, text="Currently playing: nothing")
        self.currently_playing_song.place(x=150, y=620)


        #creates and positions the play button with its image
        play_image = PhotoImage(file="play_button.png")  
        self.play_button = Button(self.master, image=play_image, command=self.play)
        self.play_button.image = play_image
        self.play_button.place(x=610, y=620)


        #creates and positions the skip forward button with its image
        skip_forward_image = PhotoImage(file="skip_forward.png")
        self.skip_forward_button = Button(self.master, image=skip_forward_image, command=self.skip_forward)
        self.skip_forward_button.image = skip_forward_image
        self.skip_forward_button.place(x=720, y=620)


        #creates and positions the skip backwards button with its image
        skip_backwards_image = PhotoImage(file="skip_backwards.png")
        self.skip_backward_button = Button(self.master, image=skip_backwards_image, command=self.skip_backward)
        self.skip_backward_button.image = skip_backwards_image
        self.skip_backward_button.place(x=480, y=620)


        #creates and positions the label for the word "volume"
        self.volume_label = Label(self.master, text="Volume")
        self.volume_label.place(x=1060,y= 590)


        #creates and positions the volume slider with it set halfway by default
        self.volume_slider = Scale(self.master, from_=0, to=100, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.place(x=1060, y=610)


        #creates and positions the label for the words "Playlists Statistsics"
        self.statistics_label = Label(self.master, text="Playlist Statistics")
        self.statistics_label.place(x=900, y=30)


        #creates and positions the statistics listbox
        self.statistics = Listbox(self.master, bg="darkgrey", width=55, height=9)
        self.statistics.place(x=900, y=65)


        #holds the playlists and songs that have been loaded
        self.stored_playlists = []
        self.stored_songs = []
       
        #holds the currently selected playlist
        self.selected_playlist = 0
        self.currently_selected_playlist = ""


        #holds the currently playing song
        self.song = ""


        #holds the length of the currently selected playlist
        self.playlist_length = 0


        #holds the times that the music was played and paused
        self.time_played = []
        self.time_paused = []
        self.time_difference = 0

        #holds the current state of the pygame mixer
        self.paused = False
        self.playing = False

    

        #initialises pygame and the pygame mixer
        pygame.init()
        pygame.mixer.init()




    #opens the playlists file and inserts all the playlists into the listbox and into the lists for storing
    def initialise_playlists(self):
        txt = []
        with open("playlists.txt", "r") as file:
            txt = file.readlines()
        for i in range(0, len(txt)):
            self.stored_playlists.insert(0, txt[i])
            self.playlist_folder.insert(0,  txt[i])
            self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))
            #insert an empty list to ensure that there is the correct number of indices for storing playlist lengths
    




    def initialise_songs(self):
        for i in range(0, len(self.stored_playlists)):
            if os.path.isfile(self.stored_playlists[i][0]+".txt"):
                with open(self.stored_playlists[i][0]+".txt", "r") as file:
                    txt=file.readlines()
                    for j in range(0, len(txt)):
                        self.stored_songs[i].append(txt[j])
            else:
                with open(self.stored_playlists[i][0]+".txt", "w") as file:
                    file.write("")
            self.time_played.append([0])
            self.time_paused.append([0])    




 
    def remove_empty_lines(self, text_file):
        with open(text_file, "r") as file:
            new_arr = []
            text = file.readlines()
            for i in range(0, len(text)):
                if text[i] != "\n":
                    new_arr.append(text[i])
        with open(text_file, "w") as file:
            file.writelines(new_arr)






    def calculate_playlist_length(self):
        try:
            num = 0
            for i in range (0, len(self.stored_songs[self.currently_selected_playlist])):
                song = self.stored_songs[self.currently_selected_playlist][i]
                if song[-1] != "3":
                    song = song[0:-1]
                try:
                    audio = (MP3("C:\\Users\\hamue\\Desktop\\New folder\\Coding-Project\\Music\\"+song)).info
                    num+=audio.length
                except:
                    pass
            
            self.playlist_length = num
        except:
            pass




    def count_time(self):
        mp3_player.calculate_playlist_length()
        minutes = round(self.playlist_length // 60)
        if minutes >= 60:
            hours = minutes // 60
            minutes = minutes % 60
        else:
            hours = 0
        seconds = round(self.playlist_length % 60)

        
        print(self.time_paused[self.selected_playlist], self.time_played[self.selected_playlist])
       

        self.statistics.insert(0, self.playlist_folder.get(self.selected_playlist) + " is " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds long")
        self.statistics.insert(1, self.time_played[self.selected_playlist])
        self.statistics.insert(2, self.time_paused[self.selected_playlist])
        self.statistics.insert(3, self.time_difference)
        self.statistics.delete(4, "end")




       
           


    def create_playlist(self):
        name = self.input_text.get(1.0, "end-1c")
        self.stored_playlists.insert(0, name)
        self.playlist_folder.insert(0, name)
        self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))
        with open("playlists.txt", "w") as file:
            for line in self.stored_playlists:
                file.write("".join(line) + "\n")


       


    def delete_playlist(self):
        self.stored_playlists.pop(self.currently_selected_playlist)
        self.stored_songs.pop(self.currently_selected_playlist)
        with open("playlists.txt", "w") as file:
            for line in self.stored_playlists:
                file.write("".join(line) + "\n")
        mp3_player.remove_empty_lines("playlists.txt")
        self.playlist_folder.delete(0, "end")
        for i in range(0, len(self.stored_playlists)):
            self.playlist_folder.insert(0, self.stored_playlists[i])
        self.playlist.delete(0, "end")
        self.playlist_label.config(text = "No playlist selected")






    def delete_song(self):
        print(self.stored_songs)
        self.stored_songs[self.currently_selected_playlist].pop(len(self.stored_songs[self.currently_selected_playlist]) - self.playlist.curselection()[0] - 1)
        with open(self.stored_playlists[self.currently_selected_playlist][0]+".txt", "w") as file:
            for line in self.stored_songs[self.currently_selected_playlist]:
                file.write("".join(line) + "\n")
        mp3_player.remove_empty_lines(self.stored_playlists[self.currently_selected_playlist][0]+".txt")
        self.playlist.delete(0, "end")
        for i in range(0, len(self.stored_songs[self.currently_selected_playlist])):
            self.playlist.insert(0, self.stored_songs[self.currently_selected_playlist][i])






    def openNewWindow(self):
        new_window = Tk()
        new_window.title("New Window")
        new_window.geometry("400x500")
        master = new_window

        load_box =  Listbox(master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=30, height=28)
        load_box.place(x=10, y=10)

        scrollbar = Scrollbar(master, width=30)
        scrollbar.place(x=300, y=100)

        load_box.config(yscrollcommand = scrollbar.set) 
        scrollbar.config(command = load_box.yview)

        search_box = Text(master, height=1, width=10)
        search_box.place(x=200, y=20)

        def add_song():
            self.playlist.insert(0, load_box.get(load_box.curselection()[0]))
            self.stored_songs[self.selected_playlist].insert(0, load_box.get(load_box.curselection()[0]))
            with open(self.stored_playlists[self.selected_playlist][0]+".txt", "w") as file:
                for line in self.stored_songs[self.selected_playlist]:
                    file.write("".join(line) + "\n")

        def search_music():
            text = search_box.get(1.0, "end-1c")
            load_box.delete(0, "end")
            for i in range(0, 100000):
                if data[14][i][0:len(text)].lower() == text.lower() or (data[14][i].lower().__contains__(text.lower()) and (len(text)-(data[14][i].lower().find(text.lower())) )**2 < 25):
                    load_box.insert(0, data[14][i])
        search_button = Button(master, text="Search", command=search_music)
        search_button.place(x=300, y=20)

        add_song_button= Button(master, text="Add song", command=add_song)
        add_song_button.place(x=300, y=60)

        data = pd.read_csv("data\\data.csv")
        data = np.array(data).T
        for i in range(0, 100):
            load_box.insert(0, data[14][i])
        
        
        




        #SOUNDRAW

    




    def select_playlist(self):
        self.selected_playlist = self.currently_selected_playlist
        mp3_player.remove_empty_lines(self.playlist_folder.get(self.selected_playlist)[0]+".txt")
        self.playlist_label.config(text = self.playlist_folder.get(self.selected_playlist))
        self.playlist.delete(0, "end")
        for i in range(0, len(self.stored_songs[self.selected_playlist])):
            self.playlist.insert(0, self.stored_songs[self.selected_playlist][i])
        






    def load_song(self):
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.playlist.insert(0, os.path.basename(file_path))
            self.stored_songs[self.selected_playlist].insert(0, os.path.basename(file_path))


            with open(self.stored_playlists[self.selected_playlist][0]+".txt", "w") as file:
                for line in self.stored_songs[self.selected_playlist]:
                    file.write("".join(line) + "\n")






    def recommend_songs(self):
        self.recommended.insert(0, "Bosh")


    def add_selected_song(self):
        self.playlist.insert(0, self.recommended.get(self.recommended.curselection()[0]))
        self.stored_songs[self.selected_playlist].insert(0, self.recommended.get(self.recommended.curselection()[0]))

        with open(self.stored_playlists[self.selected_playlist][0]+".txt", "w") as file:
            for line in self.stored_songs[self.selected_playlist]:
                file.write("".join(line) + "\n")





    def play(self):
        self.playing = True
        selected = self.playlist.get(self.playlist.curselection()[0])
        if selected[-1] != "3":
            selected = selected[0:-1]
        if self.paused == False or self.song != selected:
           
            pygame.mixer.music.load("C:\\Users\\hamue\\Desktop\\New folder\\Coding-Project\\Music\\"+selected)
            self.song = selected
            pygame.mixer.music.play()
            self.currently_playing_song.config(text="Currently Playing: " + os.path.basename(selected))
           
        elif self.paused == True:
            self.paused = False
            pygame.mixer.music.unpause()
        pause_image = PhotoImage(file="pause_button.png")
        self.play_button.config(image=pause_image, command=self.pause)
        self.play_button.image = pause_image


        self.time_played[self.selected_playlist] = (datetime.datetime.now())
       


    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
        self.playing = False
        play_image = PhotoImage(file="play_button.png")
        self.play_button.config(image=play_image, command=self.play)
        self.play_button.image = play_image


        self.time_paused[self.selected_playlist] = (datetime.datetime.now())
        





    def skip_forward(self):
        pygame.mixer.music.stop()
        self.playlist.selection_clear(0, "end")
        self.playlist.selection_set((self.playlist.curselection()[0] + 1) % self.playlist.size())
        self.play()






    def skip_backward(self):
        pygame.mixer.music.stop()
        self.playlist.selection_clear(0, "end")
        self.playlist.selection_set((self.playlist.curselection()[0] - 1) % self.playlist.size())
        self.play()






    def set_volume(self, val):
        pygame.mixer.music.set_volume(int(val) / 100)






    def check_selected_playlist(self):
        if len(self.playlist_folder.curselection()) > 0:
            self.currently_selected_playlist = self.playlist_folder.curselection()[0]
            mp3_player.select_playlist()


    



if __name__ == "__main__":
    root = Tk()
    mp3_player = MP3Player(root)
    mp3_player.remove_empty_lines("playlists.txt")
    mp3_player.initialise_playlists()
    mp3_player.initialise_songs()
    while True:
        mp3_player.check_selected_playlist()
        mp3_player.count_time()
        root.update_idletasks()
        root.update()