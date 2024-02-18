import os
import pygame


from tkinter import Tk, Button, Label, Scale, Listbox, PhotoImage, Text
from tkinter import filedialog

import LoginManager
import SearchWindow
import CalculateTime
import CreateQueue
import numpy as np
import pandas as pd


class MP3Player:
    def __init__(self, master):


        #initialise the window with its name and geometry
        self.master = master
        self.master.title("MP3 Player")
        self.master.geometry("1280x720")

        self.login_manager = LoginManager.LoginManager(self)
        self.search_window = SearchWindow.SearchWindow(self)
        self.calculate_time = CalculateTime.CalculateTime(self)
        self.create_queue = CreateQueue.CreateQueue(self)


        #creates and positions all of the buttons, listboxes, text boxes and labels for the main window's user interface
        self.create_playlist_button = Button(self.master, text="Create Playlist", command=self.create_playlist)
        self.create_playlist_button.place(x=60, y=65)

        self.delete_playlist_button = Button(self.master, text="Delete Playlist", command=self.delete_playlist)
        self.delete_playlist_button.place(x=150, y=65)

        self.playlist_label = Label(self.master, text="Playlists")
        self.playlist_label.place(x=118, y=30)

        self.playlist_folder = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkblue", width=30, height=28)
        self.playlist_folder.place(x=50, y=132)

        self.input_text = Text(height = 1, width = 22)
        self.input_text.place(x=52, y=100)

        self.playlist = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkblue", width=90, height=30)
        self.playlist.place(x=300, y=100)

        self.playlist_label = Label(self.master, text="No playlist selected")
        self.playlist_label.place(x=300, y=65)
   
        self.recommended_label = Label(self.master, text="Recommended")
        self.recommended_label.place(x=900, y=230)

        self.recommended = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkblue", width=55, height=20)
        self.recommended.place(x=900, y=260)

        self.generate_button = Button(self.master, text="Generate Songs", command=self.recommend_songs)
        self.generate_button.place(x=1140, y=225)

        self.add_song_button = Button(self.master, text="Add song", command=self.add_selected_song)
        self.add_song_button.place(x=1060, y=225)

        self.load_button = Button(self.master, text="Load Song", command=self.load_song)
        self.load_button.place(x=300, y=27)

        self.load_window = Button(self.master, text="Load Window", command=self.search_window.openNewWindow)
        self.load_window.place(x=380, y=27)

        self.delete_song_button = Button(self.master, text="Delete Song", command=self.delete_song)
        self.delete_song_button.place(x=480, y=27)

        self.currently_playing_song = Label(self.master, text="Currently playing: nothing")
        self.currently_playing_song.place(x=150, y=620)

        play_image = PhotoImage(file="play_button.png")  
        self.play_button = Button(self.master, image=play_image, command=self.play)
        self.play_button.image = play_image
        self.play_button.place(x=610, y=620)

        skip_forward_image = PhotoImage(file="skip_forward.png")
        self.skip_forward_button = Button(self.master, image=skip_forward_image, command=self.skip_forward)
        self.skip_forward_button.image = skip_forward_image
        self.skip_forward_button.place(x=720, y=620)

        skip_backwards_image = PhotoImage(file="skip_backwards.png")
        self.skip_backward_button = Button(self.master, image=skip_backwards_image, command=self.skip_backward)
        self.skip_backward_button.image = skip_backwards_image
        self.skip_backward_button.place(x=480, y=620)

        self.volume_label = Label(self.master, text="Volume")
        self.volume_label.place(x=1060,y= 590)

        self.volume_slider = Scale(self.master, from_=0, to=100, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.place(x=1060, y=610)

        self.statistics_label = Label(self.master, text="Playlist Statistics")
        self.statistics_label.place(x=900, y=30)

        self.statistics = Listbox(self.master, bg="darkgrey", width=55, height=9)
        self.statistics.place(x=900, y=65)

        self.account_button = Button(self.master, text="Accounts", command=self.login_manager.create_login_table)
        self.account_button.place(x=1170, y=27)

        self.queue_button = Button(self.master, text="Queue", command=self.create_queue.add_queue)
        self.queue_button.place(x=950, y=625)
        
        


        #holds the playlists and songs that have been loaded
        self.stored_playlists = []
        self.stored_songs = []
       
        self.song_count = 0
        self.song_score = []


        #holds the currently selected playlist
        self.selected_playlist = 0
        self.currently_selected_playlist = ""


        #holds the currently playing song
        self.song = ""


        #holds the current state of the pygame mixer
        self.freeze = True
        self.paused = True
        self.playing = False
        self.skip_used = False

        

        #initialises pygame and the pygame mixer
        pygame.init()
        pygame.mixer.init()



    #opens the playlists file and inserts all the playlists into the listbox and into the lists for storing
    def initialise_playlists(self, path):
        txt = []
        self.playlist_folder.delete(0, "end")
        with open("playlists" + path + ".txt", "r") as file:
            txt = file.readlines()
        for i in range(0, len(txt)):
            self.stored_playlists.insert(0, txt[i])
            self.playlist_folder.insert(0,  txt[i])
            self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))
            self.song_score.insert(0, 0)
            
            #insert an empty list to ensure that there is the correct number of indices for storing playlist lengths
            self.calculate_time.playlist_length.insert(0, []) 

    

    #opens each playlist file and inserts all the songs into the list of stored songs 
    def initialise_songs(self, path):
        for i in range(0, len(self.stored_playlists)):
            if os.path.isfile(self.stored_playlists[i][0]+ path +".txt"):
                with open(self.stored_playlists[i][0]+ path +".txt", "r") as file:
                    txt=file.readlines()
                    for j in range(0, len(txt)):
                        self.stored_songs[i].append(txt[j])
            else:
                #if the file doesn't exist it is created
                with open(self.stored_playlists[i][0]+ path +".txt", "w") as file:
                    file.write("")

            self.calculate_time.time_played.append([0])
            self.calculate_time.time_paused.append([0])
 
 
    #removes empty lines from the inputted file
    def remove_empty_lines(self, text_file):
        with open(text_file, "r") as file:
            new_arr = []
            text = file.readlines()
            for i in range(0, len(text)):
                if text[i] != "\n":
                    new_arr.append(text[i])
        with open(text_file, "w") as file:
            file.writelines(new_arr)
    
           
    #creates a playlist and writes the files for playlists and its songs
    def create_playlist(self):
        name = self.input_text.get(1.0, "end-1c")
        self.stored_playlists.insert(0, name)
        self.playlist_folder.insert(0, name)
        self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))
        with open("playlists" + self.login_manager.user + ".txt", "w") as file:
            for line in self.stored_playlists:
                file.write("".join(line) + "\n")
        with open(name[0] + self.login_manager.user+  ".txt", "w") as file:
            file.write("")
        self.calculate_time.playlist_length.insert(0, [])
        self.song_score.insert(0, 0)

       

    #deletes the selected playlist and sets the selected playlist back to default
    def delete_playlist(self):
        self.stored_playlists.pop(self.currently_selected_playlist)
        self.stored_songs.pop(self.currently_selected_playlist)
        with open("playlists"+ self.login_manager.user+".txt", "w") as file:
            for line in self.stored_playlists:
                file.write("".join(line) + "\n")
        mp3_player.remove_empty_lines("playlists" + self.login_manager.user + ".txt")
        self.playlist_folder.delete(0, "end")
        for i in range(0, len(self.stored_playlists)):
            self.playlist_folder.insert(0, self.stored_playlists[i])
        self.playlist.delete(0, "end")
        self.playlist_label.config(text = "No playlist selected")



    #deletes the selected song from the playlist
    def delete_song(self):
        print(self.stored_songs)
        self.stored_songs[self.currently_selected_playlist].pop(len(self.stored_songs[self.currently_selected_playlist]) - self.playlist.curselection()[0] - 1)
        with open(self.stored_playlists[self.currently_selected_playlist][0] + self.login_manager.user +".txt", "w") as file:
            for line in self.stored_songs[self.currently_selected_playlist]:
                file.write("".join(line) + "\n")
        mp3_player.remove_empty_lines(self.stored_playlists[self.currently_selected_playlist][0] + self.login_manager.user +".txt")
        self.playlist.delete(0, "end")
        for i in range(0, len(self.stored_songs[self.currently_selected_playlist])):
            self.playlist.insert(0, self.stored_songs[self.currently_selected_playlist][i])
        

    #selects the playlist the user clicks on and loads all necessary information
    def select_playlist(self):
        self.selected_playlist = self.currently_selected_playlist
        self.playlist_label.config(text = self.playlist_folder.get(self.selected_playlist))
        self.playlist.delete(0, "end")
        for i in range(0, len(self.stored_songs[self.selected_playlist])):
            self.playlist.insert(0, self.stored_songs[self.selected_playlist][i])
        


    #loads the song found in the users file exlporer into the playlist and writes the name of the song to the file
    def load_song(self):
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.playlist.insert(0, os.path.basename(file_path))
            self.stored_songs[self.selected_playlist].insert(0, os.path.basename(file_path))

            with open(self.stored_playlists[self.selected_playlist][0]+ self.login_manager.user +".txt", "w") as file:
                for line in self.stored_songs[self.selected_playlist]:
                    file.write("".join(line) + "\n")



    #loads the recommended song 
    def recommend_songs(self):
        self.recommended.delete(0, "end")
        self.data = pd.read_csv("data\\data_with_totals.csv")
        self.data = np.array(self.data).T 
        average = self.song_score[self.selected_playlist]/self.song_count
        temp = []
        for i in range(0, 170653):
            temp.append(average - self.data[15][i] + np.random.randint(-2, 2))
            
        
        for i in range(0, 5):
            self.recommended.insert(0, self.search_window.data[15][np.argmax(temp)])
            temp.pop(np.argmax(temp))


    #adds the selected song from the recommended box into the playlist and writes the song to the file
    def add_selected_song(self):
        self.playlist.insert(0, self.recommended.get(self.recommended.curselection()[0]))
        self.stored_songs[self.selected_playlist].insert(0, self.recommendusered.get(self.recommended.curselection()[0]))

        with open(self.stored_playlists[self.selected_playlist][0]+ self.login_manager.user +".txt", "w") as file:
            for line in self.stored_songs[self.selected_playlist]:
                file.write("".join(line) + "\n")


    #loads the song into the pygame music mixer and plays the song, also switches the play icon to a pause icon to indicate playing
    def play(self):
        self.playing = True
        if self.playlist.get(self.playlist.curselection()[0]) != self.create_queue.queue[self.create_queue.tail] and len(self.playlist.curselection()) > 0:
            self.create_queue.enqueue()
        selected = self.create_queue.queue[self.create_queue.tail]
        if self.skip_used == True:
            selected = self.create_queue.queue_play
            self.skip_used = False

        if selected[-1] != "3":
            selected = selected[0:-1]
        if self.paused == False or self.song != selected:
            pygame.mixer.music.load("C:\\Users\\hamue\\Desktop\\Python\\Coding-Project\\Music\\"+selected)
            self.song = selected
            pygame.mixer.music.play()
            self.currently_playing_song.config(text="Currently Playing: " + os.path.basename(selected))
        elif self.paused == True:
            self.paused = False
            pygame.mixer.music.unpause()
        pause_image = PhotoImage(file="pause_button.png")
        self.play_button.config(image=pause_image, command=self.pause)
        self.play_button.image = pause_image
        self.calculate_time.check_play_time()




    #pauses the pygame music mixer and switches the icon back to a play button
    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
        self.playing = False
        play_image = PhotoImage(file="play_button.png")
        self.play_button.config(image=play_image, command=self.play)
        self.play_button.image = play_image        

        self.calculate_time.check_pause_time()



    #skips to the next song in the queue and removes the top item
    def skip_forward(self):
        pygame.mixer.music.stop()
        self.skip_used = True
        self.queue_play = mp3_player.create_queue.dequeue()
        mp3_player.play()


    #goes back one song in the queue and adds back to the top item
    def skip_backward(self):
        pygame.mixer.music.stop()
        self.playlist.selection_clear(0, "end")
        self.playlist.selection_set((self.playlist.curselection()[0] - 1) % self.playlist.size())
        self.play()


    #sets the volume based on the volume slider
    def set_volume(self, val):
        pygame.mixer.music.set_volume(int(val) / 100)


    #checks which playlist is selected
    def check_selected_playlist(self):
        if len(self.playlist_folder.curselection()) > 0:
            self.currently_selected_playlist = self.playlist_folder.curselection()[0]
            mp3_player.select_playlist()



if __name__ == "__main__":
    #calls the functions that create the window and starts initialising the features
    root = Tk()
    mp3_player = MP3Player(root)
    mp3_player.remove_empty_lines("playlists.txt")
    mp3_player.initialise_playlists("")
    mp3_player.initialise_songs("")
    #runs the mainloop of the program and does the required checks every instance
    while True:
        mp3_player.check_selected_playlist()
        mp3_player.calculate_time.count_time()
        root.update_idletasks()
        root.update()