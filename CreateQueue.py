import customtkinter
from tkinter import Button, Listbox

class CreateQueue:
    def __init__(self, mp3_player):
    
        self.mp3_player = mp3_player
        self.master = self.mp3_player.master
        #holds queue information for operations
        self.queue_play = ""
        self.queue_length = 4
        self.queue = [None] * self.queue_length
        self.head = self.tail = -1
        self.queue_open = False
        
    #opens the queue frame and creates all the features of the queue, also loads in previously stored songs in the queue
    def add_queue(self):
        if self.queue_open == False:

            self.queue_frame = customtkinter.CTkFrame(self.master, bg_color="lightgrey",fg_color="darkgrey",
                                                       width=200, height=480, border_width=2, border_color="black")
            self.queue_frame.place(x=640,y=100)

            self.add_to_queue_button = Button(self.master, text="Add", command=self.enqueue)
            self.add_to_queue_button.place(x=650, y=110)

            self.remove_from_queue_button = Button(self.master, text="Remove", command=self.dequeue)
            self.remove_from_queue_button.place(x=700, y=110)

            self.play_queue_button = Button(self.master, text="Play", command=self.mp3_player.play)
            self.play_queue_button.place(x=780, y=110)

            self.queue_lisbox = Listbox(self.master, selectmode="SINGLE", bg="darkgrey", selectbackground="darkblue", 
                                        width=31, height=27)
            self.queue_lisbox.place(x=645, y=140)

            for i in range(self.head, self.tail):
                self.queue_lisbox.insert(0, self.queue[i])

            self.queue_open = True
        
        #closes the queue
        else:
            self.queue_frame.destroy()
            self.add_to_queue_button.destroy()
            self.remove_from_queue_button.destroy()
            self.queue_lisbox.destroy()
            self.play_queue_button.destroy()
            self.queue_open = False


    #adds a song into the queue and inserts it into the queue listbox
    def enqueue(self):
        self.playlist = self.mp3_player.playlist
        if ((self.tail + 1) % self.queue_length == self.head):
            print("The circular queue is full\n")
        elif (self.head == -1):
            self.head = 0
            self.tail = 0
            if self.mp3_player.skip_backward_used == False:
                self.queue[self.tail] = self.playlist.get(self.playlist.curselection()[0])
            else:
                self.queue[self.tail] = self.mp3_player.last_removed.pop(0)
                print(self.queue[self.tail])
            try:
                self.queue_lisbox.insert(self.tail, self.queue[self.tail])
            except:
                pass
        else:
            self.tail = (self.tail + 1) % self.queue_length
            if self.mp3_player.skip_backward_used == False:
                self.queue[self.tail] = self.playlist.get(self.playlist.curselection()[0])
            else:
                self.queue[self.tail] = self.mp3_player.last_removed.pop()
                print(self.queue[self.tail])
            try:
                self.queue_lisbox.insert(self.tail, self.queue[self.tail])
            except:
                pass


    #removes the top song from the queue and deletes it from the queue listbox
    def dequeue(self):
        if (self.head == -1):
            print("The circular queue is empty\n")

        elif (self.head == self.tail):
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            self.queue_lisbox.delete(0)
            self.mp3_player.last_removed.insert(0, temp)
            return temp

        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.queue_length
            self.queue_lisbox.delete(0)
            self.mp3_player.last_removed.insert(0, temp)
            return temp
    

