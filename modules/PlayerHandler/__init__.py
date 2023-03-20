import pygame as pg


class Player:
    def __init__(self, song_progress_bar, song_name=None):
        self.song = song_name
        self.progress_bar = song_progress_bar
        pg.mixer.init()

    def change_song(self, new_song, temp=False):
        if not temp:
            if self.song != new_song:
                if self.song:
                    pg.mixer.music.unload()
                self.progress_bar.play_len = 0
                self.song = new_song
                self.progress_bar.curr_song = self.song
                pg.mixer.music.load(f'saved\\music\\{self.song}.mp3')
                pg.mixer.music.play()
                pg.mixer.music.set_volume(0.5)
                sound = pg.mixer.Sound(f'saved\\music\\{self.song}.mp3')
                sound.stop()
                self.progress_bar.duration = pg.mixer.Sound.get_length(sound)
                self.progress_bar.render_bg()
        else:
            if self.song:
                pg.mixer.music.unload()
                self.progress_bar.play_len = 0
            self.song = new_song
            self.progress_bar.curr_song = self.song
            pg.mixer.music.load(f'saved\\temp\\{self.song}.wav')
            pg.mixer.music.play()
            pg.mixer.music.set_volume(0.5)
            sound = pg.mixer.Sound(f'saved\\temp\\{self.song}.wav')
            sound.stop()
            self.progress_bar.duration = pg.mixer.Sound.get_length(sound)
            self.progress_bar.render_bg()

    def update_bar(self):
        curr_len = pg.mixer.music.get_pos()
        if curr_len == -1:
            self.song = None
        mouse_x, mouse_y = pg.mouse.get_pos()
        if len != -1:
            self.progress_bar.render_bar(mouse_x, mouse_y, curr_len)
