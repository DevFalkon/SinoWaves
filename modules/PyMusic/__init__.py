import subprocess
import urllib.request
import re
import os
import pygame as pg
from difflib import SequenceMatcher


video_id = []
sng_info = {}


def get_name(title, query):
    if ' - ' in title:
        title = title.split(' - ')
    if type(title) == list:
        if '(' in title[1]:
            title[1] = title[1].split('(')[0]
            return title[0], title[1]
    return None


def match_query(name, query):
    return SequenceMatcher(None, name, query).ratio()


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
            process = subprocess.Popen(['utilities\\yt-dlp\\yt-dlp.exe', '--print', 'title', i],
                                       stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
            name = str(process.communicate()[0])[2:-3]
            res = get_name(name, query)
            if res:
                artist, title = res
                if match_query(title.lower(), query) > 0.7:
                    sng_info[title] = artist
                    print(sng_info)
                    break
        except Exception:
            continue


is_temp_playing = False
temp_sng = None
curr_ints = False


def inst(link, name):
    global is_temp_playing, temp_sng, curr_ints
    curr_ints = True
    try:
        subprocess.call(f'utilities\\yt-dlp\\yt-dlp.exe -o \"saved\\temp\\{name}.mp4\" {link}',
                        creationflags=subprocess.CREATE_NO_WINDOW, timeout=10)
    except subprocess.TimeoutExpired:
        print('yt-dlp timeout')
        curr_ints = False
        return

    if name == temp_sng:
        pg.mixer.music.unload()
        os.remove(f"saved\\temp\\{name}.wav")

    try:
        if f'{name}.wav' in os.listdir("saved\\temp"):
            os.remove(f"saved\\temp\\{name}.wav")
        subprocess.call(f'utilities\\ffmpeg\\ffmpeg.exe -i "saved\\temp\\{name}.mp4" "saved\\temp\\{name}.wav"',
                        creationflags=subprocess.CREATE_NO_WINDOW, timeout=5)
        os.remove(f"saved\\temp\\{name}.mp4")
        is_temp_playing = True
        temp_sng = name
        curr_ints = False
    except subprocess.TimeoutExpired:
        curr_ints = False
        print('ffmpeg timeout')
        if f'{name}.mp4' in os.listdir("saved\\temp"):
            os.remove(f"saved\\temp\\{name}.mp4")
        return


def convert(name):
    subprocess.call(f'utilities\\ffmpeg\\ffmpeg.exe -i "saved\\temp\\{name}.wav" "saved\\music\\{name}.mp3"',
                    creationflags=subprocess.CREATE_NO_WINDOW)
