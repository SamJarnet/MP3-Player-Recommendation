import datetime
from mutagen.mp3 import MP3

class CalculateTime:
    def __init__(self, mp3_player):
        self.mp3_player = mp3_player
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

    #adds up the lengths of each song in the selected playlist 
    def calculate_playlist_length(self):
        self.selected_playlist = self.mp3_player.selected_playlist

        num = 0
        for i in range (0, len(self.mp3_player.stored_songs[self.selected_playlist])):
            song = self.mp3_player.stored_songs[self.selected_playlist][i]
            if song[-1] != "3":
                song = song[0:-1]
            try:

                audio = (MP3("C:\\Users\\hamue\\Desktop\\Python\\Coding-Project\\Music\\"+song)).info
                num+=audio.length
            except:
                pass
        self.playlist_length[self.selected_playlist] = num



    def count_time(self):
        self.selected_playlist = self.mp3_player.selected_playlist
        #splits up the total time into hours minutes and seconds
        if len(self.mp3_player.playlist_folder.curselection()) > 0:
            self.calculate_playlist_length()
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
            #gets the time the playlist has been played
            mins = float(str(datetime.datetime.now())[-12:-10]) - float(str(self.start_time)[-12:-10]) - self.total_mins
            secs = float(str(datetime.datetime.now())[-9:-6]) - float(str(self.start_time)[-9:-6]) - self.total_secs
            if secs < 0:
                secs+=60
                mins-=1
        except:
            mins = 0
            secs = 0
        #displays playlist data
        self.mp3_player.statistics.insert(0, self.mp3_player.playlist_folder.get(self.selected_playlist) + " is " 
                                          + str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds long")
        if self.mp3_player.freeze == False:
            self.mp3_player.statistics.insert(1, "Total of: " + str(mins) + " minutes " + str(secs) + " seconds listened")
        else:
            self.mp3_player.statistics.insert(1, "Total of: " + str(self.saved_mins) + " minutes " + str(self.saved_secs) + " seconds listened")
        self.mp3_player.statistics.delete(2, "end")

    def check_play_time(self):
        self.selected_playlist = self.mp3_player.selected_playlist
        #gets the time that the play button is pressed and finds the time that the song was played by finding differences between start time and pasued time
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
        self.mp3_player.freeze = False

    #saves the times that the user paused the mixer to use in listening time calculations
    def check_pause_time(self):
        self.time_paused[self.selected_playlist] = (datetime.datetime.now())
        self.saved_mins = float(str(datetime.datetime.now())[-12:-10]) - float(str(self.start_time)[-12:-10]) - self.total_mins
        self.saved_secs = float(str(datetime.datetime.now())[-9:-6]) - float(str(self.start_time)[-9:-6]) - self.total_secs
        if self.saved_secs < 0:
            self.saved_secs+=60
            self.saved_mins-=1
        self.mp3_player.freeze = True