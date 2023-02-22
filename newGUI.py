import threading
from tkinter import *
from tkinter import ttk
from moviepy.video.io.VideoFileClip import VideoFileClip


class VideoEncoderGUI:
    def __init__(self, master):
        self.master = master
        self.text = Text(master)
        self.text.pack()
        
        button = ttk.Button(master, text="Start Encoding", command=self.start_encoding)
        button.pack()

    def start_encoding(self):
        self.text.insert(END, "Encoding started...\n")

        def encode():
            video = VideoFileClip("Levitico.mp4")
            video.write_videofile("output_video.mp4", verbose=False)
            self.text.insert(END, "Encoding completed!\n")

        t = threading.Thread(target=encode)
        t.start()


root = Tk()
app = VideoEncoderGUI(root)
root.mainloop()
