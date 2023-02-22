import os
import re
from moviepy.video.io.VideoFileClip import VideoFileClip


input_file_path = input("Digite o nome do Video com a extensao:\n")
#"path/to/input/video.mp4"
# Array of start times (in hour, minute, second format)
#start_times_input = input("Digite os Tempos dos Capitulos:\n")

with open('TemposIniciosCapitulos.txt', 'r') as f:
    start_times_input = [line.strip() for line in f]
start_times_input = "\n".join(start_times_input)


pattern = r'(\d{2}):(\d{2}):(\d{2})'
start_times = re.findall(pattern, start_times_input)

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
