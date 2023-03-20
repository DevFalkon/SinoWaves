import subprocess
import urllib.request
import re
import os
import pygame as pg
from pytube import YouTube


video_id = []


def web_scraper(query):
    temp = ''
    for i in query:
        if i == ' ':
            temp += '+'
        else:
            temp += i
    temp += '+song'
    html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={temp}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    vid_id = []
    for i in video_ids:
        if i not in vid_id:
            vid_id.append(i)
    if len(vid_id) > 10:
        vid_id = vid_id[0:10]
    global video_id
    video_id = vid_id
    for i in vid_id:
        try:
            vid = YouTube(f"https://www.youtube.com/watch?v={i}")
            name = vid.title
        except Exception:
            continue
        if ('concert' or 'live') not in name.lower():
            if '-' in name:
                name = name.split('-')
                if '(' in name[1]:
                    name[1] = name[1].split('(')[0]

                if name[0][-1] == ' ':
                    name[0] = name[0][:-1]
                if name[1][-1] == ' ':
                    name[1] = name[1][:-1]
                if name[1][0] == ' ':
                    name[1] = name[1][1::]
                break


is_temp_playing = False
temp_sng = None
curr_ints = False


def inst(link, name):
    global is_temp_playing, temp_sng, curr_ints
    curr_ints = True
    subprocess.call(f'utilities\\yt-dlp\\yt-dlp.exe -o \"saved\\temp\\{name}.mp4\" {link}',
                    creationflags=subprocess.CREATE_NO_WINDOW)

    if name == temp_sng:
        pg.mixer.music.unload()
        os.remove(f"saved\\temp\\{name}.wav")
    subprocess.call(f'utilities\\ffmpeg\\ffmpeg.exe -i "saved\\temp\\{name}.mp4" "saved\\temp\\{name}.wav"',
                    creationflags=subprocess.CREATE_NO_WINDOW)
    os.remove(f"saved\\temp\\{name}.mp4")
    is_temp_playing = True
    temp_sng = name
    curr_ints = False
