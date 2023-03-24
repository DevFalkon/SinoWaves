import pygame as pg
from modules.PygameGUI import widgets


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


class MusicControlButtons:
    def __init__(self):
        self.play = False

    def update(self, screen, width, height, row_r, row_spacing):
        rad = (height - 50) // 21

        if self.play:
            widgets.draw_rect(screen, width // 2 - rad,
                              int(height * (1 - row_r[2]) + 5 * row_spacing + height // 65 + 3),
                              2 * rad + 1, 2 * rad + 1, widgets.colors('blue_1'))
            pause = pg.image.load('graphics\\pause.png').convert_alpha()
            pause = pg.transform.smoothscale(pause, (2 * rad + 4, 2 * rad + 4))
            screen.blit(pause,
                        (width // 2 - rad - 2,
                         int(height * (1 - row_r[2]) + 5 * row_spacing + height // 65 + 1)))
            pg.display.update(pg.Rect(width // 2 - rad,
                                      int(height * (1 - row_r[2]) + 5 * row_spacing + height // 65 + 3),
                                      2 * rad + 2, 2 * rad + 2))

        else:
            widgets.draw_rect(screen, width // 2 - rad,
                              int(height * (1 - row_r[2]) + 5 * row_spacing + height // 65 + 3),
                              2 * rad + 1, 2 * rad + 1, widgets.colors('blue_1'))
            play = pg.image.load('graphics\\play.png').convert_alpha()
            play = pg.transform.smoothscale(play, (2 * rad + 4, 2 * rad + 4))
            screen.blit(play, (width // 2 - rad - 2,
                               int(height * (1 - row_r[2]) + 5 * row_spacing + height // 65 + 1)))
            pg.display.update(pg.Rect(width // 2 - rad,
                                      int(height * (1 - row_r[2]) + 5 * row_spacing + height // 65 + 3),
                                      2 * rad + 2, 2 * rad + 2))

        self.forward(screen, width, height, row_r, row_spacing, update=True)
        self.back(screen, width, height, row_r, row_spacing, update=True)

    def pause_play(self, screen, width, height, row_r, row_spacing):
        mouse_pos = pg.mouse.get_pos()

        rad = (height - 50) // 21
        # Pause Play button

        mouse_over_button_check = widgets.draw_circle(screen, width // 2,
                                                      int(height * (1 - row_r[
                                                          2]) + 5 * row_spacing + height // 65 + 3 + rad),
                                                      rad, widgets.colors('white'), update=False,
                                                      mouse_pos=mouse_pos)

        if mouse_over_button_check:
            if self.play:
                self.play = False
                pg.mixer.music.pause()

            else:
                self.play = True
                pg.mixer.music.unpause()

            self.update(screen, width, height, row_r, row_spacing)

    @staticmethod
    def forward(screen, width, height, row_r, row_spacing, update=False):
        mouse_pos = pg.mouse.get_pos()

        rad = (height - 50) // 22

        mouse_over_button_check = widgets.draw_circle(screen, width // 2 + 3 * rad - 5,
                                                      int(height * (1 - row_r[2]) + 6 * row_spacing +
                                                          height // 65 + 3 + rad - 5),
                                                      rad-5, widgets.colors('white'), update=False,
                                                      mouse_pos=mouse_pos)

        if update:
            widgets.draw_rect(screen, width // 2 + 2 * rad,
                              int(height * (1 - row_r[2]) + 6 * row_spacing + height // 65 + 3),
                              2 * rad - 10, 2 * rad - 10, widgets.colors('blue_1'))
            forward = pg.image.load('graphics\\forward.png').convert_alpha()
            forward = pg.transform.smoothscale(forward, (2 * rad - 10, 2 * rad - 10))
            screen.blit(forward, (width // 2 + 2 * rad,
                                  int(height * (1 - row_r[2]) + 6 * row_spacing + height // 65 + 3)))
            pg.display.update(pg.Rect(width // 2 + 2 * rad,
                                      int(height * (1 - row_r[2]) + 6 * row_spacing + height // 65 + 3),
                                      2 * rad - 10, 2 * rad - 10))

        else:
            if mouse_over_button_check:
                return True
            return False

    @staticmethod
    def back(screen, width, height, row_r, row_spacing, update=False):
        mouse_pos = pg.mouse.get_pos()

        rad = (height - 50) // 22

        mouse_over_button_check = widgets.draw_circle(screen, width // 2 - 3.7 * rad + rad - 5,
                                                      int(height * (1 - row_r[2]) +
                                                          6 * row_spacing + height // 65 + 3 + rad - 5),
                                                      rad-5, widgets.colors('red'), update=False,
                                                      mouse_pos=mouse_pos)

        if update:
            widgets.draw_rect(screen, width // 2 - 3.7 * rad,
                              int(height * (1 - row_r[2]) + 6 * row_spacing + height // 65 + 3),
                              2 * rad - 10, 2 * rad - 10, widgets.colors('blue_1'))
            back = pg.image.load('graphics\\back.png').convert_alpha()
            back = pg.transform.smoothscale(back, (2 * rad - 10, 2 * rad - 10))
            screen.blit(back, (width // 2 - 3.7 * rad,
                               int(height * (1 - row_r[2]) + 6 * row_spacing + height // 65 + 3)))
            pg.display.update(pg.Rect(width // 2 - 3.7 * rad,
                                      int(height * (1 - row_r[2]) + 6 * row_spacing + height // 65 + 3),
                                      2 * rad - 10, 2 * rad - 10))

        else:
            if mouse_over_button_check:
                return True
            return False
