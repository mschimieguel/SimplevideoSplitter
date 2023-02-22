from datetime import datetime, timedelta

start_times = ["00:00:00", "00:03:19", "00:06:32", "00:09:39", "00:16:34", "00:21:31", "00:27:35", "00:34:37", "00:41:18", "00:45:34", "00:50:34", "00:58:49", "01:00:45", "01:12:47", "01:23:47", "01:29:26", "01:37:05", "01:40:30", "01:45:21", "01:52:09", "01:58:07", "02:02:16", "02:08:30", "02:17:14", "02:21:10", "02:31:25", "02:40:29"]

# Convert the time strings to datetime objects
times = [datetime.strptime(time, '%H:%M:%S') for time in start_times]

# Initialize variables for the start and end times of the current chapter
chapter_start = times[0]
chapter_end = times[0]

# Iterate over pairs of consecutive times and check if the duration between them is at most 25 minutes
for i in range(len(times) - 1):
    for j in range(1,len(times) - 1):
        duration = times[i+1] - times[i]
        






    
    if duration <= timedelta(minutes=25):
        # The duration between consecutive times is at most 25 minutes, so the current chapter has not ended
        chapter_end = times[i+1]
    else:
        # The duration between consecutive times is more than 25 minutes, so the current chapter has ended
        print(f"Chapter from {chapter_start.strftime('%H:%M:%S')} to {chapter_end.strftime('%H:%M:%S')}: {chapter_end - chapter_start}")
        chapter_start = times[i+1]
        chapter_end = times[i+1]

# Print the final chapter
print(f"Chapter from {chapter_start.strftime('%H:%M:%S')} to {times[-1].strftime('%H:%M:%S')}: {times[-1] - chapter_start}")
