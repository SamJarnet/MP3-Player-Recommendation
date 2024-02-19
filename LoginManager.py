import sqlite3
import bcrypt
import customtkinter
from tkinter import messagebox

class LoginManager:
        def __init__(self, mp3_player):
            self.mp3_player = mp3_player
            #inititialises the sql database
            self.conn = sqlite3.connect("logins.db")
            self.cursor = self.conn.cursor()
            self.login_created = False
            self.user = ""

        def create_login_table(self):
            if self.login_created == False:
                #creates the database
                self.login_created = True
                self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
                
                #creates all the features of the login frame
                self.frame1 = customtkinter.CTkFrame(self.mp3_player.master, bg_color="lightgrey",fg_color="darkgrey", width=720, height=480, border_width=5, border_color="black")
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
            #gets inputs and checks them in the database for exisisting cases
            username = self.username_entry.get()
            password = self.password_entry.get()
            if username != "" and password != "":
                self.cursor.execute("SELECT username FROM users WHERE username=?", [username])
                if self.cursor.fetchone() is not None:
                    messagebox.showerror("Error", "Username already exists")
                else:
                    #hashes the password so they cannot be accessed
                    encoded_password = password.encode("utf-8")
                    hashed_password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
                    self.cursor.execute("INSERT INTO users VALUES (?, ?)", [username, hashed_password])
                    self.conn.commit()
                    #show success message
                    messagebox.showinfo("Success", "Account has been created.")
            else:
                #show error in case of mistake 
                messagebox.showerror("Error", "Enter all data.")


        def login_account(self):
            #gets inputs and checks if they exist in the database
            username = self.username_entry2.get()
            password = self.password_entry2.get()
            #checks if the hashed input is the same as the hashed password for the respective password
            if username != "" and password != "":
                self.cursor.execute("SELECT password FROM users WHERE username=?", [username]) 
                result = self.cursor.fetchone()
                if result:
                    if bcrypt.checkpw(password.encode("utf-8"), result[0]):
                        #load the mp3 player for the user that logged in
                        self.frame2.destroy()
                        self.login_created = False
                        self.mp3_player.stored_playlists = []
                        self.mp3_player.stored_songs = []
                        self.user = username 
                        self.mp3_player.playlist.delete(0, "end")
                        try:
                            self.mp3_player.initialise_playlists(username)
                            self.mp3_player.initialise_songs(username)
                        except:
                            with open("playlists" + username + ".txt", "w") as file:
                                file.write("")
                            self.mp3_player.initialise_playlists(username)
                            self.mp3_player.initialise_songs(username)

                    else:
                        messagebox.showerror("Error", "Invalid password.")
                else:
                    messagebox.showerror("Error", "Invalid username.")
            else:
                messagebox.showerror("Error", "Enter all data.")


        def login(self):
            #loads login frame with login features
            self.frame1.destroy()
            self.frame2 = customtkinter.CTkFrame(self.mp3_player.master, bg_color="lightgrey",fg_color="darkgrey", width=720, height=480, border_width=5, border_color="black")
            self.frame2.place(x=280,y=100)

            login_label2 = customtkinter.CTkLabel(self.frame2, text="Log in")
            login_label2.place(x=280, y=20)
        
            self.username_entry2 = customtkinter.CTkEntry(self.frame2, placeholder_text="Username", width=100, height=5)
            self.username_entry2.place(x=230, y=80)

            self.password_entry2 = customtkinter.CTkEntry(self.frame2, show="*", placeholder_text="Password", width=100, height=5)
            self.password_entry2.place(x=230, y=150)

            login_button2 = customtkinter.CTkButton(self.frame2, command=self.login_account, text="Login", width=10, height=2)
            login_button2.place(x=230, y=220)