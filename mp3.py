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
        # Set up main window
        self.master = master
        self.master.title("MP3 Player")
        self.master.geometry("1280x720")

        # Initialize helper classes
        self.login_manager = LoginManager.LoginManager(self)
        self.search_window = SearchWindow.SearchWindow(self)
        self.calculate_time = CalculateTime.CalculateTime(self)
        self.create_queue = CreateQueue.CreateQueue(self)

        # Create buttons and UI elements
        self.create_playlist_button = Button(
            self.master, text="Create Playlist", command=self.create_playlist)
        self.create_playlist_button.place(x=60, y=65)

        self.delete_playlist_button = Button(
            self.master, text="Delete Playlist", command=self.delete_playlist)
        self.delete_playlist_button.place(x=150, y=65)

        self.playlist_label = Label(self.master, text="Playlists")
        self.playlist_label.place(x=118, y=30)

        self.playlist_folder = Listbox(
            self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkblue", width=30, height=28)
        self.playlist_folder.place(x=50, y=132)

        self.input_text = Text(height=1, width=22)
        self.input_text.place(x=52, y=100)

        self.playlist = Listbox(self.master, selectmode="SINGLE",
                                bg="darkgrey", selectbackground="darkblue", width=90, height=30)
        self.playlist.place(x=300, y=100)

        self.playlist_label = Label(self.master, text="No playlist selected")
        self.playlist_label.place(x=300, y=65)

        self.recommended_label = Label(self.master, text="Recommended")
        self.recommended_label.place(x=900, y=230)

        self.recommended = Listbox(self.master, selectmode="SINGLE",
                                   bg="darkgrey", selectbackground="darkblue", width=55, height=20)
        self.recommended.place(x=900, y=260)

        self.generate_button = Button(
            self.master, text="Generate Songs", command=self.recommend_songs)
        self.generate_button.place(x=1140, y=225)

        self.add_song_button = Button(
            self.master, text="Add song", command=self.add_song)
        self.add_song_button.place(x=1060, y=225)

        self.load_button = Button(
            self.master, text="Load Song", command=self.load_song)
        self.load_button.place(x=300, y=27)

        self.load_window = Button(
            self.master, text="Load Window", command=self.search_window.openNewWindow)
        self.load_window.place(x=380, y=27)

        self.delete_song_button = Button(
            self.master, text="Delete Song", command=self.delete_song)
        self.delete_song_button.place(x=480, y=27)

        self.currently_playing_song = Label(
            self.master, text="Currently playing: nothing")
        self.currently_playing_song.place(x=150, y=620)

        # Set up play/pause and skip buttons with images
        play_image = PhotoImage(file="assets\\play_button.png")
        self.play_button = Button(
            self.master, image=play_image, command=self.play)
        self.play_button.image = play_image
        self.play_button.place(x=610, y=620)

        skip_forward_image = PhotoImage(file="assets\\skip_forward.png")
        self.skip_forward_button = Button(
            self.master, image=skip_forward_image, command=self.skip_forward)
        self.skip_forward_button.image = skip_forward_image
        self.skip_forward_button.place(x=720, y=620)

        skip_backwards_image = PhotoImage(file="assets\\skip_backwards.png")
        self.skip_backward_button = Button(
            self.master, image=skip_backwards_image, command=self.skip_backward)
        self.skip_backward_button.image = skip_backwards_image
        self.skip_backward_button.place(x=480, y=620)

        # Volume control slider
        self.volume_label = Label(self.master, text="Volume")
        self.volume_label.place(x=1060, y=590)

        self.volume_slider = Scale(
            self.master, from_=0, to=100, orient="horizontal", command=self.set_volume)
        self.volume_slider.set(50)
        self.volume_slider.place(x=1060, y=610)

        self.statistics_label = Label(self.master, text="Playlist Statistics")
        self.statistics_label.place(x=900, y=30)

        self.statistics = Listbox(
            self.master, bg="darkgrey", width=55, height=9)
        self.statistics.place(x=900, y=65)

        self.account_button = Button(
            self.master, text="Accounts", command=self.login_manager.create_login_table)
        self.account_button.place(x=1170, y=27)

        self.queue_button = Button(
            self.master, text="Queue", command=self.create_queue.add_queue)
        self.queue_button.place(x=950, y=625)

        # Lists to store playlists and songs
        self.stored_playlists = []
        self.stored_songs = []

        # Tracking variables
        self.song_score = []
        self.selected_playlist = 0
        self.currently_selected_playlist = 0
        self.song = ""

        self.paused = True
        self.playing = False
        self.freeze = True

        # Load song features dataset
        self.dataset = pd.read_csv("data/data.csv", low_memory=False)

        pygame.init()
        pygame.mixer.init()

    def initialise_playlists(self, username):
        # Load playlist names from file and show in listbox
        self.playlist_folder.delete(0, "end")
        self.stored_playlists.clear()
        self.stored_songs.clear()
        self.song_score.clear()
        self.calculate_time.playlist_length.clear()

        filepath = f"playlists\\playlists{username}.txt"
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                pass

        with open(filepath, "r") as file:
            lines = file.readlines()

        for line in lines:
            playlist_name = line.strip()
            if playlist_name:
                self.stored_playlists.append(playlist_name)
                self.playlist_folder.insert("end", playlist_name)
                self.stored_songs.append([])
                self.song_score.append(0)
                self.calculate_time.playlist_length.append([])

    def initialise_songs(self, path):
        # Load songs for each playlist
        for i, playlist_name in enumerate(self.stored_playlists):
            song_file = f"playlists\\{playlist_name}{path}.txt"
            if os.path.isfile(song_file):
                with open(song_file, "r") as file:
                    songs = [line.strip() for line in file if line.strip()]
                    self.stored_songs[i] = songs
            else:
                with open(song_file, "w") as file:
                    pass
            self.calculate_time.time_played.append([0])
            self.calculate_time.time_paused.append([0])

    def remove_empty_lines(self, text_file):
        # Remove empty lines from a file
        with open(text_file, "r") as file:
            lines = [line for line in file if line.strip()]
        with open(text_file, "w") as file:
            file.writelines(lines)

    def create_playlist(self):
        # Create new playlist and update file
        name = self.input_text.get(1.0, "end-1c").strip()
        if not name:
            return
        self.stored_playlists.insert(0, name)
        self.playlist_folder.insert(0, name)
        self.stored_songs.insert(0, [])
        self.song_score.insert(0, 0)
        self.calculate_time.playlist_length.insert(0, [])

        filepath = f"playlists\\playlists{self.login_manager.user}.txt"
        with open(filepath, "w") as file:
            for pl in self.stored_playlists:
                file.write(pl + "\n")

        with open(f"playlists\\{name}{self.login_manager.user}.txt", "w") as file:
            pass

    def delete_playlist(self):
        # Remove selected playlist and update file & UI
        if self.currently_selected_playlist >= len(self.stored_playlists):
            return
        self.stored_playlists.pop(self.currently_selected_playlist)
        self.stored_songs.pop(self.currently_selected_playlist)

        filepath = f"playlists\\playlists{self.login_manager.user}.txt"
        with open(filepath, "w") as file:
            for pl in self.stored_playlists:
                file.write(pl + "\n")

        self.remove_empty_lines(filepath)
        self.playlist_folder.delete(0, "end")
        for pl in self.stored_playlists:
            self.playlist_folder.insert("end", pl)
        self.playlist.delete(0, "end")
        self.playlist_label.config(text="No playlist selected")

    def delete_song(self):
        # Delete selected song from current playlist
        if not self.playlist.curselection():
            return
        index = self.playlist.curselection()[0]
        playlist_songs = self.stored_songs[self.currently_selected_playlist]
        if index >= len(playlist_songs):
            return
        playlist_songs.pop(index)

        filepath = f"playlists\\{self.stored_playlists[self.currently_selected_playlist]}{self.login_manager.user}.txt"
        with open(filepath, "w") as file:
            for song in playlist_songs:
                file.write(song + "\n")

        self.remove_empty_lines(filepath)

        self.playlist.delete(0, "end")
        for song in playlist_songs:
            self.playlist.insert("end", song)

    def select_playlist(self):
        # Show songs from selected playlist
        self.selected_playlist = self.currently_selected_playlist
        self.playlist_label.config(
            text=self.playlist_folder.get(self.selected_playlist))
        self.playlist.delete(0, "end")
        for song in self.stored_songs[self.selected_playlist]:
            self.playlist.insert("end", song)

    def load_song(self):
        # Load song from file dialog into current playlist
        file_path = filedialog.askopenfilename(
            defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            song_name = os.path.basename(file_path)
            self.playlist.insert("end", song_name)
            self.stored_songs[self.selected_playlist].append(song_name)

            filepath = f"playlists\\{self.stored_playlists[self.selected_playlist]}{self.login_manager.user}.txt"
            with open(filepath, "w") as file:
                for song in self.stored_songs[self.selected_playlist]:
                    file.write(song + "\n")

    def get_playlist_feature_vectors(self):
        # Get features for songs in current playlist
        playlist_songs = [s.strip()
                          for s in self.stored_songs[self.selected_playlist]]
        df = self.dataset[self.dataset["name"].isin(playlist_songs)]
        if df.empty:
            return np.array([])
        features = ["valence", "year", "acousticness", "danceability", "duration_ms", "energy",
                    "explicit", "instrumentalness", "key", "liveness", "loudness", "mode",
                    "popularity", "speechiness", "tempo"]
        return df[features].to_numpy()

    def get_average_feature_vector(self):
        # Average feature vector for playlist songs
        vectors = self.get_playlist_feature_vectors()
        if len(vectors) == 0:
            return None
        return np.mean(vectors, axis=0)

    def recommend_songs(self):
        # Recommend top 5 similar songs not already in playlist
        self.recommended.delete(0, "end")
        avg_vector = self.get_average_feature_vector()
        if avg_vector is None:
            print("No valid songs found in dataset.")
            return

        playlist_songs = [s.strip()
                          for s in self.stored_songs[self.selected_playlist]]
        features = ["valence", "year", "acousticness", "danceability", "duration_ms", "energy",
                    "explicit", "instrumentalness", "key", "liveness", "loudness", "mode",
                    "popularity", "speechiness", "tempo"]

        candidate_songs = self.dataset[~self.dataset["name"].isin(
            playlist_songs)].copy()
        candidate_vectors = candidate_songs[features].to_numpy()

        # Calculate cosine similarity
        similarities = np.dot(candidate_vectors, avg_vector) / (
            np.linalg.norm(candidate_vectors, axis=1) * np.linalg.norm(avg_vector))

        candidate_songs["similarity"] = similarities
        top_matches = candidate_songs.sort_values(
            by="similarity", ascending=False).head(5)

        for _, row in top_matches.iterrows():
            self.recommended.insert("end", row["name"])

    def add_song(self):
        # Add selected recommended song to playlist and save
        if not self.recommended.curselection():
            return
        song = self.recommended.get(self.recommended.curselection()[0])
        self.playlist.insert("end", song)
        self.stored_songs[self.selected_playlist].append(song)

        filepath = f"playlists\\{self.stored_playlists[self.selected_playlist]}{self.login_manager.user}.txt"
        with open(filepath, "w") as file:
            for s in self.stored_songs[self.selected_playlist]:
                file.write(s + "\n")

        self.remove_empty_lines(filepath)

    def play(self):
        # Play selected song, or resume if paused
        self.playing = True
        if len(self.playlist.curselection()) == 0:
            return
        selected_song = self.playlist.get(self.playlist.curselection()[0])
        song_path = "Music\\" + selected_song
        if self.paused or self.song != selected_song:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            self.song = selected_song
            self.paused = False
            self.currently_playing_song.config(
                text="Currently Playing: " + selected_song)
        else:
            pygame.mixer.music.unpause()

        pause_image = PhotoImage(file="assets\\pause_button.png")
        self.play_button.config(image=pause_image, command=self.pause)
        self.play_button.image = pause_image
        self.calculate_time.check_play_time()

    def pause(self):
        # Pause the music
        pygame.mixer.music.pause()
        self.paused = True
        self.playing = False

        play_image = PhotoImage(file="assets\\play_button.png")
        self.play_button.config(image=play_image, command=self.play)
        self.play_button.image = play_image
        self.calculate_time.check_pause_time()

    def skip_forward(self):
        # Skip to next song
        pygame.mixer.music.stop()
        self.skip_forward_used = True
        self.play()

    def skip_backward(self):
        # Skip to previous song
        pygame.mixer.music.stop()
        self.skip_backward_used = True
        self.play()

    def set_volume(self, val):
        # Set volume based on slider
        pygame.mixer.music.set_volume(int(val) / 100)

    def check_selected_playlist(self):
        # Update selected playlist index when user clicks
        if len(self.playlist_folder.curselection()) > 0:
            self.currently_selected_playlist = self.playlist_folder.curselection()[
                0]
            self.select_playlist()


if __name__ == "__main__":
    # Start the app
    root = Tk()
    mp3_player = MP3Player(root)

    mp3_player.remove_empty_lines("playlists\\playlists.txt")
    mp3_player.initialise_playlists("")
    mp3_player.initialise_songs("")

    while True:
        mp3_player.check_selected_playlist()
        mp3_player.calculate_time.count_time()
        root.update_idletasks()
        root.update()
