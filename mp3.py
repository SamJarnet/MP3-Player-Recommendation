import os
import pygame
from tkinter import Tk, Frame, Button, Label, Scale, Listbox, StringVar, PhotoImage
from tkinter import filedialog

class MP3Player:
    def __init__(self, master):
        self.master = master
        self.master.title("MP3 Player")
        self.master.geometry("1280x720")

        self.playlist_folder = Listbox(self.master, selectmode="SINGLE", bg="lightgrey", selectbackground="darkred", width=30, height=30)
        self.playlist_folder.place(x=50, y=100)

        self.playlist = Listbox(self.master, selectmode="SINGLE", bg="lightgrey", selectbackground="darkred", width=90, height=30)
        self.playlist.place(x=300, y=100)

        self.recommended_label = Label(self.master, text="Recommended")
        self.recommended_label.place(x=900, y=230)
        self.recommended = Listbox(self.master, selectmode="SINGLE", bg="lightgrey", selectbackground="darkred", width=55, height=20)
        self.recommended.place(x=900, y=260)
        self.generate_button = Button(self.master, text="Generate Songs", command=self.recommend_songs)
        self.generate_button.place(x=1140, y=225)

        self.load_button = Button(self.master, text="Load Song", command=self.load_song)
        self.load_button.place(x=300, y=30)

        self.currently_playing_song = Label(self.master, text="Currently playing: nothing")
        self.currently_playing_song.place(x=150, y=620)


        play_image = PhotoImage(file="play_button.png")  
        self.play_button = Button(self.master, image=play_image, command=self.play)
        self.play_button.image = play_image
        self.play_button.place(x=610, y=620)

        self.pause_button = Button(self.master, text="Pause", command=self.pause)
        self.pause_button.place(x=610, y=700)

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

        self.current_song = StringVar()

        pygame.init()
        pygame.mixer.init()

    def load_song(self):
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])

        if file_path:
            self.playlist.insert(0, os.path.basename(file_path))
            pygame.mixer.music.load(file_path)
    
    def recommend_songs(self):
        self.recommended.insert(0, "randomtext")


    def play(self):
        pygame.mixer.music.play()
        self.currently_playing_song.config(text="Currently Playing: " + os.path.basename(self.playlist.get(0)))

    def pause(self):
        pygame.mixer.music.pause()
        self.current_song.set("Paused: " + os.path.basename(self.playlist.get(0)))

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

if __name__ == "__main__":
    root = Tk()
    mp3_player = MP3Player(root)
    root.mainloop()
