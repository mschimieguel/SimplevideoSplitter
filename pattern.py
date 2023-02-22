import re

pattern = r'(\d{2}):(\d{2}):(\d{2})'
start_times_input = '''Cap. 01 - 00:00:00                        
Cap. 02 - 00:03:19
Cap. 03 - 00:06:32
Cap. 04 - 00:09:39
Cap. 05 - 00:16:34
Cap. 06 - 00:21:31
Cap. 07 - 00:27:35
Cap. 08 - 00:34:37
Cap. 09 - 00:41:18
Cap. 10 - 00:45:34
Cap. 11 - 00:50:34
Cap. 12 - 00:58:49
Cap. 13 - 01:00:45
Cap. 14 - 01:12:47
Cap. 15 - 01:23:47
Cap. 16 - 01:29:26
Cap. 17 - 01:37:05
Cap. 18 - 01:40:30
Cap. 19 - 01:45:21
Cap. 20 - 01:52:09
Cap. 21 - 01:58:07
Cap. 22 - 02:02:16
Cap. 23 - 02:08:30
Cap. 24 - 02:17:14
Cap. 25 - 02:21:10
Cap. 26 - 02:31:25
Cap. 27 - 02:40:29'''

# extract start times from input using regex
start_times = re.findall(pattern, start_times_input)

for i,time in enumerate(start_times):
    start_times[i] = ":".join(time)

print(start_times)