import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import subprocess
import re
from moviepy.video.io.VideoFileClip import VideoFileClip


def video_spliter(start_times,input_file_path):
    
    for i,time in enumerate(start_times):
        start_times[i] = ":".join(time)
    #juntarCapitulos = input("Deseja Juntar Capitulos ?(S para sim )")


    #start_times = ["00:00:00", "00:03:19", "00:06:32", "00:09:39", "00:16:34", "00:21:31", "00:27:35", "00:34:37", "00:41:18", "00:45:34", "00:50:34", "00:58:49", "01:00:45", "01:12:47", "01:23:47", "01:29:26", "01:37:05", "01:40:30", "01:45:21", "01:52:09", "01:58:07", "02:02:16", "02:08:30", "02:17:14", "02:21:10", "02:31:25"]

    # Path to the input video file

    # Path to the output directory for the chapter files
    if(not os.path.exists("Capitulos/")):
        os.makedirs("Capitulos")
    output_dir_path = "Capitulos/"

    # Load the video file and get its total duration in seconds
    video = VideoFileClip(input_file_path)
    total_duration = video.duration

    # Loop through each start time, extract the corresponding chapter from the video,
    # and save it to a separate file in the output directory
    for i, start_time in enumerate(start_times):
        if i == len(start_times) - 1:
            # Last chapter: extract until the end of the video
            end_time = total_duration
        else:
            # Regular chapter: extract until the start of the next chapter
            end_time = start_times[i+1]
        output_file_path = os.path.join(output_dir_path, f"{input_file_path.split('.')[0]} Capítulo {i+1}.mp4")
        clip = video.subclip(start_time, end_time)
        clip.write_videofile(output_file_path)

# Create a new Tkinter window
window = tk.Tk()
window.title("My Window")

# Create a label widget
label = tk.Label(window, text="Choose a video file:")
label.pack()

# Create a canvas widget to display the video thumbnail
canvas = tk.Canvas(window, width=320, height=240)
canvas.pack()

# Create a label widget to display the selected file name
selected_file_label = tk.Label(window, text="")
selected_file_label.pack()

# Create a button widget to open a file dialog
selected_file_path=""
def choose_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename()
    selected_file_name = os.path.basename(selected_file_path)
    selected_file_label.configure(text="Selected file: " + selected_file_name)
    
    # Generate a thumbnail image from the video file
    cap = cv2.VideoCapture(selected_file_path)
    
    # Set the video capture's position to the 1 second mark
    cap.set(cv2.CAP_PROP_POS_MSEC, 1000)
    
    # Read the next frame
    ret, frame = cap.read()
    
    # Check if the frame is valid
    if ret:
        # Convert the image from BGR to RGB color space
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Resize the frame to the canvas size
        thumbnail = cv2.resize(frame, (320, 240))
        
        # Convert the OpenCV image to a PIL Image object
        img = Image.fromarray(thumbnail)
        
        # Convert the PIL Image object to a PhotoImage object
        img_tk = ImageTk.PhotoImage(img)
        
        # Display the image on the canvas
        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        
        # Save the image reference to prevent garbage collection
        canvas.img_tk = img_tk
    
    cap.release()

browse_button = tk.Button(window, text="Browse", command=choose_file)
browse_button.pack()

# Create a second label widget and a scrolled text input widget
label2 = tk.Label(window, text="Enter some text:")
label2.pack()
text_input = scrolledtext.ScrolledText(window, height=8, width=50)
text_input.pack(fill="both", expand=True)

def run_command():
    pattern = r'(\d{2}):(\d{2}):(\d{2})'
    start_times = re.findall(pattern, text_input.get("1.0", "end-1c"))
    
    print(start_times)
    print(text_input.get("1.0", "end-1c"))
    if (selected_file_path == ""):
        messagebox.showwarning("No File Selected", "Please select a file before running the command.")
        return
    if ( len(start_times) <= 0 ):
        messagebox.showwarning("Sem Tempos de Capitulos", "Please select a file before running the command.")
        return
    video_spliter(start_times,selected_file_path)
    # command = text_input.get("1.0", "end-1c")
    # result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #output_text.delete("1.0", "end")
    #output_text.insert("1.0", result.stdout.decode('utf-8', errors='ignore') + result.stderr.decode('utf-8', errors='ignore'))

run_button = tk.Button(window, text="Run", command=run_command, bg="green", fg="white")
run_button.pack()

# Create a scrolled text widget to display the output
output_text = scrolledtext.ScrolledText(window, height=8, width=50)
output_text.pack(fill="both", expand=True)

# Run the main event loop
window.mainloop()
