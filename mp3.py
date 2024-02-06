import os
import pygame
from tkinter import Tk, Frame, Button, Label, Scale, Listbox, StringVar, PhotoImage, Text, Toplevel, Scrollbar, messagebox
from tkinter import filedialog
from mutagen.mp3 import MP3
import datetime
import numpy as np
import pandas as pd
import customtkinter
import sqlite3
import bcrypt

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

        #creates account button to open the login/sign in system
        self.account_button = Button(self.master, text="Accounts", command=self.create_login_table)
        self.account_button.place(x=1170, y=27)

        #creates the queue button to open the queue frame
        self.queue_button = Button(self.master, text="Queue", command=self.add_queue)
        self.queue_button.place(x=950, y=625)
        
        self.queue_play = ""
        self.queue_length = 15
        self.queue = [None] * self.queue_length
        self.head = self.tail = -1

        #holds the playlists and songs that have been loaded
        self.stored_playlists = []
        self.stored_songs = []
       
        #holds the currently selected playlist
        self.selected_playlist = 0
        self.currently_selected_playlist = ""


        #holds the currently playing song
        self.song = ""


        #holds the length of the currently selected playlist
        self.playlist_length = []


        #holds the times that the music was played and paused
        self.time_played = []
        self.time_paused = []
        self.time_difference = 0
        self.start_time = datetime.datetime.now()
        self.total_mins = 0
        self.total_secs = 0
        self.saved_mins = 0
        self.saved_secs = 0

        #holds the current state of the pygame mixer
        self.freeze = True
        self.paused = True
        self.playing = False
        self.queue_open = False

        self.conn = sqlite3.connect("logins.db")
        self.cursor = self.conn.cursor()
        
        self.login_created = False
        self.user = ""

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
            self.playlist_length.insert(0, [])
            self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))

            #insert an empty list to ensure that there is the correct number of indices for storing playlist lengths
    


    def initialise_songs(self, path):
        for i in range(0, len(self.stored_playlists)):
            if os.path.isfile(self.stored_playlists[i][0]+ path +".txt"):
                with open(self.stored_playlists[i][0]+ path +".txt", "r") as file:
                    txt=file.readlines()
                    for j in range(0, len(txt)):
                        self.stored_songs[i].append(txt[j])
            else:
                with open(self.stored_playlists[i][0]+ path +".txt", "w") as file:
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


    def create_login_table(self):
        if self.login_created == False:
            self.login_created = True
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)''')
            self.frame1 = customtkinter.CTkFrame(self.master, bg_color="lightgrey",fg_color="darkgrey", width=720, height=480, border_width=10, border_color="black")
            self.frame1.place(x=280,y=100)
            
            signup_label = customtkinter.CTkLabel(self.frame1, text="Sign up", width=10, height=2)
            signup_label.place(x=280, y=20)

            self.username_entry = customtkinter.CTkEntry(self.frame1, placeholder_text="Username", width=100, height=5)
            self.username_entry.place(x=230, y=80)

            self.password_entry = customtkinter.CTkEntry(self.frame1, show="*", placeholder_text="Password", width=100, height=5)
            self.password_entry.place(x=230, y=150)

            signup_button = customtkinter.CTkButton(self.frame1, command=self.signup, text="Sign up", width=10, height=2)
            signup_button.place(x=230, y=220)

            login_label = customtkinter.CTkLabel(self.frame1, text="Already have an account?", width=10, height=2)
            login_label.place(x=230, y=250)

            login_button = customtkinter.CTkButton(self.frame1, command=self.login, text="Login", width=10, height=2)
            login_button.place(x=395, y=250)


    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username != "" and password != "":
            self.cursor.execute("SELECT username FROM users WHERE username=?", [username])
            if self.cursor.fetchone() is not None:
                messagebox.showerror("Error", "Username already exists")
            else:
                encoded_password = password.encode("utf-8")
                hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                self.cursor.execute("INSERT INTO users VALUES (?, ?)", [username, hashed_password])
                self.conn.commit()
                messagebox.showinfo("Success", "Account has been created.")
        else:
            messagebox.showerror("Error", "Enter all data.")


    def login_account(self):
        username = self.username_entry2.get()
        password = self.password_entry2.get()
        if username != "" and password != "":
            self.cursor.execute("SELECT password FROM users WHERE username=?", [username]) 
            result = self.cursor.fetchone()
            if result:
                if bcrypt.checkpw(password.encode("utf-8"), result[0]):
                    self.frame2.destroy()
                    self.login_created = False
                    self.stored_playlists = []
                    self.stored_songs = []
                    self.user = username 
                    self.playlist.delete(0, "end")
                    try:
                        mp3_player.initialise_playlists(username)
                        mp3_player.initialise_songs(username)
                    except:
                        with open("playlists" + username + ".txt", "w") as file:
                            file.write("")
                        mp3_player.initialise_playlists(username)
                        mp3_player.initialise_songs(username)

                else:
                    messagebox.showerror("Error", "Invalid password.")
            else:
                messagebox.showerror("Error", "Invalid username.")
        else:
            messagebox.showerror("Error", "Enter all data.")


    def login(self):
        self.frame1.destroy()
        self.frame2 = customtkinter.CTkFrame(self.master, bg_color="lightgrey",fg_color="darkgrey", width=720, height=480, border_width=10, border_color="black")
        self.frame2.place(x=280,y=100)

        login_label2 = customtkinter.CTkLabel(self.frame2, text="Log in")
        login_label2.place(x=280, y=20)

    
        self.username_entry2 = customtkinter.CTkEntry(self.frame2, placeholder_text="Username", width=100, height=5)
        self.username_entry2.place(x=230, y=80)

        self.password_entry2 = customtkinter.CTkEntry(self.frame2, show="*", placeholder_text="Password", width=100, height=5)
        self.password_entry2.place(x=230, y=150)

        login_button2 = customtkinter.CTkButton(self.frame2, command=self.login_account, text="Login", width=10, height=2)
        login_button2.place(x=230, y=220)


    def calculate_playlist_length(self):
      
        num = 0
        for i in range (0, len(self.stored_songs[self.currently_selected_playlist])):
            song = self.stored_songs[self.currently_selected_playlist][i]
            if song[-1] != "3":
                song = song[0:-1]
            try:
                audio = (MP3("C:\\Users\\hamue\\Desktop\\New Folder\\Coding-Project\\Music\\"+song)).info
                num+=audio.length
            except:
                pass
        
        self.playlist_length[self.selected_playlist] = num


    def count_time(self):
        if len(self.playlist_folder.curselection()) > 0:
            mp3_player.calculate_playlist_length()
            minutes = round(self.playlist_length[self.selected_playlist] // 60)
        
            if minutes >= 60:
                hours = minutes // 60
                minutes = minutes % 60
            else:
                hours = 0
            seconds = round(self.playlist_length[self.selected_playlist] % 60)
        else:
            hours, minutes, seconds = 0, 0 , 0

        try:
            mins = float(str(datetime.datetime.now())[-12:-10]) - float(str(self.start_time)[-12:-10]) - self.total_mins
            secs = float(str(datetime.datetime.now())[-9:-6]) - float(str(self.start_time)[-9:-6]) - self.total_secs
            if secs < 0:
                secs+=60
                mins-=1
        except:
            mins = 0
            secs = 0
        self.statistics.insert(0, self.playlist_folder.get(self.selected_playlist) + " is " + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds long")
        self.statistics.insert(1, datetime.datetime.now()-self.start_time)
        self.statistics.insert(2, str(self.total_mins) + " " + str(self.total_secs))
        if self.freeze == False:
            self.statistics.insert(3, str(mins) + " minutes " + str(secs)  )
        else:
            self.statistics.insert(3, str(self.saved_mins) + " minutes " + str(self.saved_secs))
        self.statistics.delete(4, "end")


           

    def create_playlist(self):
        name = self.input_text.get(1.0, "end-1c")
        self.stored_playlists.insert(0, name)
        self.playlist_folder.insert(0, name)
        self.stored_songs.insert(0,(list(self.playlist_folder.get(0, -1))))
        with open("playlists" + self.user + ".txt", "w") as file:
            for line in self.stored_playlists:
                file.write("".join(line) + "\n")
        with open(name[0] + self.user+  ".txt", "w") as file:
            file.write("")
        self.playlist_length.insert(0, [])

       


    def delete_playlist(self):
        self.stored_playlists.pop(self.currently_selected_playlist)
        self.stored_songs.pop(self.currently_selected_playlist)
        with open("playlists"+ self.user+".txt", "w") as file:
            for line in self.stored_playlists:
                file.write("".join(line) + "\n")
        mp3_player.remove_empty_lines("playlists" + self.user + ".txt")
        self.playlist_folder.delete(0, "end")
        for i in range(0, len(self.stored_playlists)):
            self.playlist_folder.insert(0, self.stored_playlists[i])
        self.playlist.delete(0, "end")
        self.playlist_label.config(text = "No playlist selected")




    def delete_song(self):
        print(self.stored_songs)
        self.stored_songs[self.currently_selected_playlist].pop(len(self.stored_songs[self.currently_selected_playlist]) - self.playlist.curselection()[0] - 1)
        with open(self.stored_playlists[self.currently_selected_playlist][0] + self.user +".txt", "w") as file:
            for line in self.stored_songs[self.currently_selected_playlist]:
                file.write("".join(line) + "\n")
        mp3_player.remove_empty_lines(self.stored_playlists[self.currently_selected_playlist][0] + self.user +".txt")
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

        info_box = Listbox(master, height=14, width = 30)
        info_box.place(x=200, y=200)

        self.searched_songs = []


        def add_song():
            self.playlist.insert(0, load_box.get(load_box.curselection()[0]))
            self.stored_songs[self.selected_playlist].insert(0, load_box.get(load_box.curselection()[0]))
            with open(self.stored_playlists[self.selected_playlist][0]+ self.user +".txt", "w") as file:
                for line in self.stored_songs[self.selected_playlist]:
                    file.write("".join(line) + "\n")

        def show_info():
            print(self.searched_songs)
            info_box.delete(0, "end")
            artists = data[16][self.searched_songs[load_box.curselection()[0]]]
            artists = artists.replace("[", "")
            artists = artists.replace("]", "")
            artists = artists.split(",")
            year = str(int(data[1][self.searched_songs[load_box.curselection()[0]]]*2020))
            for i in range(0, len(artists)):
                info_box.insert(i,"Artist: " + artists[i])
            info_box.insert(len(artists)+1, "Year: " + year)

        def search_music():
            text = search_box.get(1.0, "end-1c")
            load_box.delete(0, "end")
            self.searched_songs = []
            for i in range(0, 100000):
                if data[15][i][0:len(text)].lower() == text.lower() or (data[15][i].lower().__contains__(text.lower()) and (len(text)-(data[15][i].lower().find(text.lower())) )**2 < 25 and len(text) > 2):
                    self.searched_songs.insert(0, i)
                    load_box.insert(0, data[15][i])
        search_button = Button(master, text="Search", command=search_music)
        search_button.place(x=300, y=20)

        add_song_button= Button(master, text="Add song", command=add_song)
        add_song_button.place(x=300, y=60)

        show_info_button = Button(master, text="Show information", command=show_info)
        show_info_button.place(x=300, y=100)

        

        data = pd.read_csv("data\\data.csv")
        data = np.array(data).T
        for i in range(0, 100):
            load_box.insert(0, data[15][i])
            self.searched_songs.insert(0, i)
        


    def select_playlist(self):
        self.selected_playlist = self.currently_selected_playlist
        mp3_player.remove_empty_lines(self.playlist_folder.get(self.selected_playlist)[0]+ self.user + ".txt")
        self.playlist_label.config(text = self.playlist_folder.get(self.selected_playlist))
        self.playlist.delete(0, "end")
        for i in range(0, len(self.stored_songs[self.selected_playlist])):
            self.playlist.insert(0, self.stored_songs[self.selected_playlist][i])
        



    def load_song(self):
        file_path = filedialog.askopenfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.playlist.insert(0, os.path.basename(file_path))
            self.stored_songs[self.selected_playlist].insert(0, os.path.basename(file_path))


            with open(self.stored_playlists[self.selected_playlist][0]+ self.user +".txt", "w") as file:
                for line in self.stored_songs[self.selected_playlist]:
                    file.write("".join(line) + "\n")




    def recommend_songs(self):
        self.recommended.insert(0, "Bosh")



    def add_selected_song(self):
        self.playlist.insert(0, self.recommended.get(self.recommended.curselection()[0]))
        self.stored_songs[self.selected_playlist].insert(0, self.recommendusered.get(self.recommended.curselection()[0]))

        with open(self.stored_playlists[self.selected_playlist][0]+ self.user +".txt", "w") as file:
            for line in self.stored_songs[self.selected_playlist]:
                file.write("".join(line) + "\n")



    def play(self):
        self.playing = True
        print(self.queue[self.tail])
        if self.playlist.get(self.playlist.curselection()[0]) != self.queue[self.tail] and len(self.playlist.curselection()) > 0:
            self.enqueue()
        
        
        selected = self.queue[self.tail]
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
        try: 
            self.time_difference = self.time_played[self.selected_playlist] -self.time_paused[self.selected_playlist]
        except:
            self.time_difference = datetime.datetime.now()-datetime.datetime.now()
        try: 
            if str(self.time_difference)[0] != "-":
                self.total_mins += float(str(self.time_difference)[-12:-10])
                self.total_secs += float(str(self.time_difference)[-9:-6])
                if self.total_secs > 60:
                    self.total_secs -= 60
                    self.total_mins += 1
            else:
                self.total_mins += 0
                self.total_secs += 0
        except:
            pass
        self.freeze = False



    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
        self.playing = False
        play_image = PhotoImage(file="play_button.png")
        self.play_button.config(image=play_image, command=self.play)
        self.play_button.image = play_image

        self.time_paused[self.selected_playlist] = (datetime.datetime.now())
        self.saved_mins = float(str(datetime.datetime.now())[-12:-10]) - float(str(self.start_time)[-12:-10]) - self.total_mins
        self.saved_secs = float(str(datetime.datetime.now())[-9:-6]) - float(str(self.start_time)[-9:-6]) - self.total_secs
        if self.saved_secs < 0:
            self.saved_secs+=60
            self.saved_mins-=1
        self.freeze = True



    def add_queue(self):
        if self.queue_open == False:

            self.queue_frame = customtkinter.CTkFrame(self.master, bg_color="lightgrey",fg_color="darkgrey", width=200, height=480, border_width=2, border_color="black")
            self.queue_frame.place(x=640,y=100)

            self.add_to_queue_button = Button(self.master, text="Add", command=self.enqueue)
            self.add_to_queue_button.place(x=650, y=110)

            self.remove_from_queue_button = Button(self.master, text="Remove", command=self.dequeue)
            self.remove_from_queue_button.place(x=700, y=110)

            self.play_queue_button = Button(self.master, text="Play", command=self.play)
            self.play_queue_button.place(x=780, y=110)

            self.queue_lisbox = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkred", width=31, height=27)
            self.queue_lisbox.place(x=645, y=140)

            for i in range(self.head, self.tail):
                self.queue_lisbox.insert(0, self.queue[i])

            self.queue_open = True
            
        else:
            self.queue_frame.destroy()
            self.add_to_queue_button.destroy()
            self.remove_from_queue_button.destroy()
            self.queue_lisbox.destroy()
            self.play_queue_button.destroy()
            self.queue_open = False



    def enqueue(self):
        if ((self.tail + 1) % self.queue_length == self.head):
            print("The circular queue is full\n")
        elif (self.head == -1):
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = self.playlist.get(self.playlist.curselection()[0])
            try:
                self.queue_lisbox.insert(0, self.playlist.get(self.playlist.curselection()[0]))
            except:
                pass
        else:
            self.tail = (self.tail + 1) % self.queue_length
            self.queue[self.tail] = self.playlist.get(self.playlist.curselection()[0])
            try:
                self.queue_lisbox.insert(0, self.playlist.get(self.playlist.curselection()[0]))
            except:
                pass


    def dequeue(self):
        if (self.head == -1):
            print("The circular queue is empty\n")

        elif (self.head == self.tail):
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            self.queue_lisbox.delete(0)
            return temp

        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.queue_length
            self.queue_lisbox.delete(0)
            print(self.queue)
            return temp
        

    def skip_forward(self):
        pygame.mixer.music.stop()
        self.queue_play = mp3_player.dequeue()
        mp3_player.play()



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
    #mp3_player.create_login_table()
    mp3_player.remove_empty_lines("playlists.txt")
    mp3_player.initialise_playlists("")
    mp3_player.initialise_songs("")
    while True:
        mp3_player.check_selected_playlist()
        mp3_player.count_time()
        root.update_idletasks()
        root.update()