import os
import pygame
from tkinter import Tk, Frame, Button, Label, Scale, Listbox, StringVar, PhotoImage, Text
from tkinter import filedialog
from mutagen.mp3 import MP3

class MP3Player:
    def __init__(self, master):
        self.master = master
        self.master.title("MP3 Player")
        self.master.geometry("1280x720")
        

        self.create_playlist_button = Button(self.master, text="Create Playlist", command=self.create_playlist)
        self.create_playlist_button.place(x=100, y=65)
        self.playlist_label = Label(self.master, text="Playlists")
        self.playlist_label.place(x=118, y=30)
        self.playlist_folder = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=30, height=28)
        self.playlist_folder.place(x=50, y=132)
        self.input_text = Text(height = 1, width = 22)
        self.input_text.place(x=52, y=100)

        self.playlist = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=90, height=30)
        self.playlist.place(x=300, y=100)
        self.playlist_label = Label(self.master, text="No playlist selected")
        self.playlist_label.place(x=300, y=65)
   

        self.recommended_label = Label(self.master, text="Recommended")
        self.recommended_label.place(x=900, y=230)
        self.recommended = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=55, height=20)
        self.recommended.place(x=900, y=260)
        self.generate_button = Button(self.master, text="Generate Songs", command=self.recommend_songs)
        self.generate_button.place(x=1140, y=225)

        self.load_button = Button(self.master, text="Load Song", command=self.load_song)
        self.load_button.place(x=300, y=27)

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

        self.stored_playlists = []
        self.stored_songs = []
        
        self.selected_playlist = 0
        self.currently_selected_playlist = ""
        self.song = ""
        self.playlist_length = 0

        self.paused = False

        pygame.init()
        pygame.mixer.init()


    def load_playlists(self):
        txt = []
        with open("playlists.txt", "r") as file:
            txt = file.readlines()
        for i in range(0, len(txt)):
            self.stored_playlists.insert(0, txt[i])
            self.playlist_folder.insert(0,  txt[i])
            self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))

    def create_playlist(self):
        name = self.input_text.get(1.0, "end-1c")
        self.stored_playlists.insert(0, name)
        self.playlist_folder.insert(0, name)
        self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))
        with open("playlists.txt", "w") as file:
            for line in self.stored_playlists:
                file.write("".join(line) + "\n")


    def select_playlist(self):
        self.selected_playlist = self.currently_selected_playlist
        self.playlist_label.config(text = self.playlist_folder.get(self.selected_playlist))
        self.playlist.delete(0, "end")
        for i in range(0, len(self.stored_songs[self.selected_playlist])):
            self.playlist.insert(0, self.stored_songs[self.selected_playlist][i])


    def load_song(self):
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.playlist.insert(0, os.path.basename(file_path))
            # pygame.mixer.music.load(file_path)
            length = MP3(file_path).info.length
            self.stored_songs[self.selected_playlist].insert(0, os.path.basename(file_path))
           
            self.playlist_length += length
            self.statistics.delete(0, "end")
            self.statistics.insert(0, str(self.playlist_length)[0:6] + " seconds long")

    def recommend_songs(self):
        self.recommended.insert(0, "randomtext")


    def play(self):
        if self.paused == False or self.song != self.playlist.get(self.playlist.curselection()[0]):
            pygame.mixer.music.load("C:/Users/hamue/Downloads/"+self.playlist.get(self.playlist.curselection()[0]))
            self.song = self.playlist.get(self.playlist.curselection()[0])
            pygame.mixer.music.play()
            self.currently_playing_song.config(text="Currently Playing: " + os.path.basename(self.playlist.get(self.playlist.curselection()[0])))
        elif self.paused == True:
            self.paused = False
            pygame.mixer.music.unpause()
        pause_image = PhotoImage(file="pause_button.png")
        self.play_button.config(image=pause_image, command=self.pause)
        self.play_button.image = pause_image

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
        play_image = PhotoImage(file="play_button.png")
        self.play_button.config(image=play_image, command=self.play)
        self.play_button.image = play_image

    def skip_forward(self):
        pygame.mixer.music.stop()
        self.playlist.selection_clear(0, "end")
        self.playlist.selection_set((self.playlist.curselection() + 1) % self.playlist.size())
        self.play()

    def skip_backward(self):
        pygame.mixer.music.stop()
        self.playlist.selection_clear(0, "end")
        self.playlist.selection_set((self.playlist.curselection() - 1) % self.playlist.size())
        self.play()

    def set_volume(self, val):
        pygame.mixer.music.set_volume(int(val) / 100)


    def check_selected_playlist(self):
        if len(self.playlist_folder.curselection()) > 0:
            self.currently_selected_playlist = self.playlist_folder.curselection()[0]
            mp3_player.select_playlist()
    def check_selected_song(self):
        if len(self.playlist.curselection()) > 0:
            pass


if __name__ == "__main__":
    root = Tk()
    mp3_player = MP3Player(root)
    mp3_player.load_playlists()
    while True:
        mp3_player.check_selected_playlist()
        root.update_idletasks()
        root.update()
        
        
    
