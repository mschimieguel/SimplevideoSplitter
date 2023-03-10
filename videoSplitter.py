import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext
import os
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import subprocess
import re
from moviepy.video.io.VideoFileClip import VideoFileClip
import sys
from io import StringIO

# global list to store all threads
threads = []
stdout_io = StringIO()
stderr_io = StringIO()
sys.stdout = stdout_io
sys.stderr = stderr_io



def on_closing():
    # iterate through all threads and join them
    #for t in threads:
    #    t.join()
        
    # destroy the main window and exit the program
    window.destroy()
    sys.exit()

def video_spliter(start_times,video,input_file_path,output_dir_path):
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
        #print(output_dir_path)
        #print(f"{input_file_path.split('.')[0]} Capítulo {i+1}.mp4")    
        output_file_path = os.path.join(output_dir_path, f"{input_file_path.split('/')[-1].split('.')[0]} Capítulo {i+1}.mp4")
        #print(output_file_path)
        clip = video.subclip(start_time, end_time)
        clip.write_videofile(output_file_path)
        print("*****************Video Completamente Dividido - Operacao Finalizada*****************")
    sys.exit()

def write_to_console(message):
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, message)

# Create a new Tkinter window
window = tk.Tk()
window.title("Video Splitter - Particionador de Videos")


# Redirect stdout and stderr to a file
output_file = open("console_output.txt", "w+")
sys.stdout = output_file
sys.stderr = output_file

selected_file_path=""

def choose_file():
    global selected_file_path
    selected_file_path = filedialog.askopenfilename()
    selected_file_name = os.path.basename(selected_file_path)
    if(selected_file_path != ""):
        selected_file_label.configure(text="Video Selecionado: " + selected_file_name,fg="green")
        canvas.configure(width=200, height=150)
        
        
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
        thumbnail = cv2.resize(frame, (200, 150))
        
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

label = tk.Label(window, text="Escolha um Video Para Dividir:")
label.pack()



browse_button = tk.Button(window, text="Selecionar Video", command=choose_file,bg="green",fg="white")
browse_button.pack()

selected_file_label = tk.Label(window, text="")
selected_file_label.pack()

# Create a canvas widget to display the video thumbnail
canvas = tk.Canvas(window,width=0, height=0)
canvas.pack()

# Create a second label widget and a scrolled text input widget
label2 = tk.Label(window, text="Coloque aqui os momentos que deja cortar o video (formato hh:mm:ss)\n ")
label2.pack()
text_input = scrolledtext.ScrolledText(window, height=12, width=30)
text_input.pack(fill="both", expand=True)

def run_command():
 
    pattern = r'(\d{2}):(\d{2}):(\d{2})'
    start_times = re.findall(pattern, text_input.get("1.0", "end-1c"))
    
    #print(start_times)
    #print(text_input.get("1.0", "end-1c"))
    if (selected_file_path == ""):
        messagebox.showwarning("Nenhum Video Selecionado", "Por Favor Escolha um Video")
        return
    if ( len(start_times) <= 0 ):
        messagebox.showwarning("Sem Tempos de Capitulos", "Por favor Coloque os tempos em que se deseja dividir o video")
        return
    
    #sys.stdout.write = write_to_console
    #sys.stderr.write = write_to_console

    for i,time in enumerate(start_times):
        start_times[i] = ":".join(time)

    file_name = selected_file_path.split('/')[-1].split('.')[0]
    # Path to the output directory for the chapter files
    
    output_dir_path = os.path.join(  os.path.dirname(selected_file_path),f"Capitulos_{file_name}/")
    output_dir_path = output_dir_path.replace('\\','/')
    if(not os.path.exists(output_dir_path)):
        os.makedirs(output_dir_path)
    #print(output_dir_path)

    # Load the video file and get its total duration in seconds
    video = VideoFileClip(selected_file_path)
    t = threading.Thread(target=video_spliter, args=(start_times,video,selected_file_path,output_dir_path),daemon=True)
    t.start()
    # add the thread to the global list
    threads.append(t)

    #video_spliter(start_times,video,output_dir_path)
    # command = text_input.get("1.0", "end-1c")
    # result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #output_text.delete("1.0", "end")
    #output_text.insert("1.0", result.stdout.decode('utf-8', errors='ignore') + result.stderr.decode('utf-8', errors='ignore'))

run_button = tk.Button(window, text="Dividir Video", command=run_command, bg="green", fg="white")
run_button.pack()

def clear_text(widget):
    widget.delete("1.0", tk.END)
    widget.after(500, clear_text, widget)

def update_output_text():
    # Read the contents of the output file
    with open("console_output.txt", "r") as f:
        output = f.readlines()
    output = output[-1] if output else ""
    output= output.replace("|1","|\u258F")
    output= output.replace("|2","|\u258E")
    output= output.replace("|3","|\u258D")
    output= output.replace("|4","|\u258D")
    output= output.replace("|5","|\u258C")
    output= output.replace("|6","|\u258C")
    output= output.replace("|7","|\u258B")
    output= output.replace("|8","|\u258A")
    output= output.replace("|9","|\u2589")
    output= output.replace("#1","#\u258F")
    output= output.replace("#2","#\u258E")
    output= output.replace("#3","#\u258D")
    output= output.replace("#4","#\u258D")
    output= output.replace("#5","#\u258C")
    output= output.replace("#6","#\u258C")
    output= output.replace("#7","#\u258B")
    output= output.replace("#8","#\u258A")
    output= output.replace("#9","#\u2589")


    output = output.replace('#', '\u2588')
    #output = output_file.read()
    #output= output[-1]
    
    # Update the output_text widget with the contents of the output file
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, output)
    window.after(100, update_output_text)
    # Schedule the update_output_text function to be called again in 100 milliseconds    

# Create a scrolled text widget to display the output
output_text = scrolledtext.ScrolledText(window, height=1, width=30,fg="green")
#output_text.pack()
output_text.pack(fill="both", expand=True)



# Start the recursive update_console_output() function
update_output_text()

#clear_text(output_text)

# create a function to handle window closing
window.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main event loop
window.mainloop()
