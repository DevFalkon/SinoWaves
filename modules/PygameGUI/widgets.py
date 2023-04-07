import time
import pygame as pg
from pygame import gfxdraw
import math


def draw_circle(screen, centre_x, centre_y, radius, color, update=True, mouse_pos=None):
    centre_x = int(centre_x)
    centre_y = int(centre_y)
    radius = int(radius)
    gfxdraw.aacircle(screen, centre_x, centre_y, radius, color)
    gfxdraw.filled_circle(screen, centre_x, centre_y, radius, color)
    if update:
        pg.display.update(pg.Rect(centre_x - radius - 1, centre_y - radius, 2 * radius + 2, 2 * radius + 2))
    if mouse_pos:
        dist = math.sqrt(math.pow(mouse_pos[0] - centre_x, 2) + math.pow(mouse_pos[1] - centre_y, 2))
        if dist <= radius:
            return True
        return False


def draw_rect(screen, top_x, top_y, width, height, color, update=True, mouse_pos=None):
    pg.draw.rect(screen, color, pg.Rect(top_x, top_y, width, height))
    if update:
        pg.display.update(pg.Rect(top_x, top_y, width, height))
    if mouse_pos:
        if top_x <= mouse_pos[0] <= top_x + width and \
                top_y <= mouse_pos[1] <= top_y + height:
            return True
        return False


def colors(color):
    colors_dict = {
        'red': (235, 18, 7),
        'green': (74, 222, 16),
        'yellow': (235, 200, 7),
        'grey': (61, 61, 61),
        'light_grey': (163, 160, 158),
        'white': (255, 255, 255),
        'dark_grey': (41, 41, 41),
        'blue_1': (121, 121, 121),
        'black': (0, 0, 0)
    }
    return colors_dict[color]


def rounded_rect(screen, top_x, top_y, width, height, radius, color, bg_color='dark_grey',
                 update=True, mouse_pos=None):
    if bg_color:
        draw_rect(screen, top_x, top_y, width, height, colors(bg_color), update=False)
    if not mouse_pos:
        draw_circle(screen, top_x + radius, top_y + radius, radius, color, update=False)
        draw_circle(screen, top_x + width - radius - 1, top_y + radius, radius, color, update=False)
        draw_circle(screen, top_x + radius, top_y + height - radius - 1, radius, color, update=False)
        draw_circle(screen, top_x + width - radius - 1, top_y + height - radius - 1, radius, color, update=False)

        draw_rect(screen, top_x + radius, top_y + radius, width - 2 * radius, height - 2 * radius, color, update=False)

        draw_rect(screen, top_x, top_y + radius + 2, radius, height - 2 * radius - 2, color, update=False)
        draw_rect(screen, top_x + width - radius, top_y + radius + 2, radius, height - 2 * radius - 2, color,
                  update=False)
        draw_rect(screen, top_x + radius + 2, top_y, width - 2 * radius - 2, radius, color, update=False)
        draw_rect(screen, top_x + radius + 2, top_y + height - radius, width - 2 * radius - 2, radius, color,
                  update=False)

    if mouse_pos:
        c1 = draw_circle(screen, top_x + radius, top_y + radius, radius, color, update=False,
                         mouse_pos=mouse_pos)
        c2 = draw_circle(screen, top_x + width - radius - 1, top_y + radius, radius, color, update=False,
                         mouse_pos=mouse_pos)
        c3 = draw_circle(screen, top_x + radius, top_y + height - radius - 1, radius, color, update=False,
                         mouse_pos=mouse_pos)
        c4 = draw_circle(screen, top_x + width - radius - 1, top_y + height - radius - 1, radius, color, update=False,
                         mouse_pos=mouse_pos)

        c5 = draw_rect(screen, top_x + radius, top_y + radius, width - 2 * radius, height - 2 * radius, color,
                       update=False, mouse_pos=mouse_pos)

        c6 = draw_rect(screen, top_x, top_y + radius + 2, radius, height - 2 * radius - 2, color, update=False,
                       mouse_pos=mouse_pos)
        c7 = draw_rect(screen, top_x + width - radius, top_y + radius + 2, radius, height - 2 * radius - 2, color,
                       update=False, mouse_pos=mouse_pos)
        c8 = draw_rect(screen, top_x + radius + 2, top_y, width - 2 * radius - 2, radius, color, update=False,
                       mouse_pos=mouse_pos)
        c9 = draw_rect(screen, top_x + radius + 2, top_y + height - radius, width - 2 * radius - 2, radius, color,
                       update=False, mouse_pos=mouse_pos)

        if c1 or c2 or c3 or c4 or c5 or c6 or c7 or c8 or c9:
            return True
        return False

    if update:
        pg.display.update(pg.Rect(top_x, top_y, width, height))


class SearchBar:
    def __init__(self, screen, top_x, top_y, width, height, bg_color='dark_grey'):
        self.screen = screen
        self.top_x = top_x
        self.top_y = top_y
        self.width = width
        self.height = height
        self.rad = height // 2
        draw_rect(screen, top_x, top_y, width, height, colors(bg_color))
        draw_rect(self.screen, self.top_x + self.rad + 2, self.top_y, self.width - 2 * self.rad - 4, self.height,
                  (255, 255, 255), update=False)
        draw_circle(self.screen, self.top_x + self.rad, self.top_y + self.rad, self.rad,
                    (255, 255, 255), update=False)
        draw_circle(self.screen, self.top_x + self.width - self.rad, self.top_y + self.rad, self.rad,
                    (255, 255, 255), update=False)
        self.is_active = False
        self.font_size = self.height - 15
        self.font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', self.font_size)
        self.text = 'Search   '
        self.render_text()
        pg.display.update(pg.Rect(top_x, top_y, width + 10, height))
        self.cnt = 0

    def activate(self, mouse_pos, bttn):
        c1 = draw_rect(self.screen, self.top_x + self.rad + 2, self.top_y, self.width - 2 * self.rad - 4, self.height,
                       (255, 255, 255), update=False, mouse_pos=mouse_pos)
        c2 = draw_circle(self.screen, self.top_x + self.rad, self.top_y + self.rad, self.rad,
                         (255, 255, 255), update=False, mouse_pos=mouse_pos)
        c3 = draw_circle(self.screen, self.top_x + self.width - self.rad, self.top_y + self.rad, self.rad,
                         (255, 255, 255), update=False, mouse_pos=mouse_pos)

        if (c1 or c2 or c3) and bttn and not self.is_active:
            self.is_active = True
            self.text = ''

    def render_text(self):
        if self.text == 'Search   ':
            col = 'light_grey'
        else:
            col = 'grey'
        text = self.font.render(self.text, True, colors(col))
        self.screen.blit(text, (self.top_x + self.rad,
                                self.top_y + 3))
        pg.display.update(pg.Rect(self.top_x + self.rad, self.top_y, self.width - 2 * self.rad, self.height))

    def type(self, key):
        if self.is_active:
            if key:
                if self.text != '' and key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if key == pg.K_SPACE:
                        self.text += ' '
                    key = pg.key.name(key)
                    if len(key) == 1:
                        self.text += key
                self.render_text()


class Button:
    def __init__(self, screen, top_x, top_y, width, height, rad, color, text="button", bg_col="dark_grey",
                 font_col='white'):
        self.screen = screen
        self.top_x = top_x
        self.top_y = top_y
        self.width = width
        self.height = height
        self.rad = rad
        self.color = color
        self.text = text
        rounded_rect(self.screen, self.top_x, self.top_y, self.width, self.height, self.rad, self.color,
                     bg_color=bg_col)
        font_size = self.height // 2
        font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', font_size)
        text_sr = font.render(text, True, colors(font_col))
        text_width = text_sr.get_width()
        self.screen.blit(text_sr, (self.top_x + self.width // 2 - text_width // 2,
                                   self.top_y + (self.height - font_size) // 2 - 3))
        pg.display.update(pg.Rect(self.top_x, self.top_y, self.width, self.height))

    def get_pressed(self, mouse_pos):
        if rounded_rect(self.screen, self.top_x, self.top_y, self.width, self.height, self.rad, self.color,
                        mouse_pos=mouse_pos, update=False):
            return self.text


class Scroll:
    def __init__(self, screen, top_x, top_y, width, height, iterable, app_window_height) -> None:
        self.screen = screen
        self.iterable = iterable
        self.iterable = sorted(self.iterable)

        # Scrollable text position and dimension
        self.top_x = top_x
        self.top_y = top_y
        self.width = width
        self.height = height

        self.initial_y = top_y

        self.background_color = 'dark_grey'

        self.scroll = 0
        self.scroll_sens = 20

        self.spacer = 2

        self.elem_height = app_window_height // 16
        self.font_size = self.elem_height - 12

    # to get maximum nuber of rows that can be displayed at once
    def get_max_rows(self):
        max_row = (self.height) // (self.spacer + self.elem_height)
        return max_row

    # To find the y coordinate when the last button is completely visible
    def get_max_y(self):
        if len(self.iterable) > self.get_max_rows():
            low = self.scroll + self.top_y + len(self.iterable) * (self.spacer + self.elem_height)
            return low
        return None

    def render(self):
        font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', self.font_size)
        draw_rect(self.screen, self.top_x, self.top_y, self.width, self.height,
                  colors(self.background_color),
                  update=False)
        for ind, elem in enumerate(self.iterable):
            if self.top_y - self.elem_height <= self.top_y + self.scroll + ind * (
                    self.spacer + self.elem_height) < self.top_y + self.height:
                # Drawing the seperator for each button
                draw_rect(self.screen, self.top_x + 2,
                          self.top_y + self.scroll +
                          ind * (self.spacer + self.elem_height) + self.elem_height,
                          self.width - 4, self.spacer, colors('white'), update=False)

                text = font.render(str(elem), True, colors('white'))
                self.screen.blit(text, (self.top_x + 10,
                                        self.top_y + self.scroll +
                                        ind * (self.spacer + self.elem_height)))

            # to reduce no of iterations
            if self.top_y + self.scroll + ind * (self.spacer + self.elem_height) > \
                    self.top_y + self.height:
                break
        pg.display.update(pg.Rect(self.top_x, self.initial_y, self.width, self.height))

    def update(self, ev=None):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.top_x + 2 <= mouse_x <= self.top_x + self.width - 4 and self.top_y <= mouse_y <= \
                self.top_y + self.height:
            max_y = self.get_max_y()
            if self.get_max_rows() < len(self.iterable) and max_y >= self.top_y + self.height:
                if ev and self.scroll <= 0:
                    self.scroll += ev * self.scroll_sens
            else:
                pass

            if self.scroll > 0:
                self.scroll = 0

            max_y = self.get_max_y()
            if max_y:
                while max_y < self.top_y + self.height:
                    self.scroll += 1
                    max_y = self.get_max_y()
            self.render()

    def get_name(self):
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.top_x + 2 <= mouse_x <= self.top_x + self.width - 4 and self.top_y <= mouse_y <= \
                self.top_y + self.height:
            for ind, elem in enumerate(self.iterable):
                if self.top_y + self.scroll + ind * (self.spacer + self.elem_height) <= mouse_y <= \
                        self.top_y + self.scroll + ind * (self.spacer + self.elem_height) + self.elem_height:
                    return elem
        return None

    def force_update(self):
        self.render()


class PlayerProgressBar:

    def __init__(self, screen, top_x, top_y, width, height) -> None:
        self.bar_len = 0
        self.seek = None
        self.play_len = 0
        self.screen = screen
        self.width = width
        self.height = height
        self.curr_song = None
        self.duration = 0
        self.prev_pos = 0
        self.top_x = top_x
        self.top_y = top_y
        draw_rect(self.screen, self.top_x, self.top_y, self.width, self.height, colors('grey'))

    def render_bg(self):
        draw_rect(self.screen, self.top_x, self.top_y, self.width, self.height, colors('grey'))

    def render_bar(self, mouse_x, mouse_y, len_played):
        if self.curr_song:
            self.prev_pos = len_played
            if len_played == -1:
                self.curr_song = None
                draw_rect(self.screen, self.top_x, self.top_y, self.width, self.height, colors('grey'))
                self.duration = 0
                self.prev_pos = 0
                self.bar_len = 0
                self.play_len = 0
                return
            self.bar_len = ((self.width) / (self.duration)) * (len_played / 1000) + self.play_len
            if self.bar_len > self.width:
                self.bar_len = self.width
            draw_rect(self.screen, self.top_x, self.top_y, self.bar_len, self.height, colors('white'))
            if self.top_x <= mouse_x <= self.top_x + self.width - 1 and \
                    self.top_y <= mouse_y <= self.top_y + self.height:
                if pg.mouse.get_pressed()[0]:
                    pg.mixer.music.set_volume(0)
                    pg.mixer.music.rewind()
                    self.play_len -= self.bar_len
                    pos = ((mouse_x - self.top_x) * self.duration) / (self.width)
                    pg.mixer.music.set_pos(pos)
                    time.sleep(0.02)
                    self.play_len += mouse_x - self.top_x
                    draw_rect(self.screen, self.top_x, self.top_y, self.width, self.height, colors('grey'))
                    pg.mixer.music.set_volume(0.5)


class VolumeControl():
    def __init__(self, screen, top_x, top_y, width, height):
        self.bar_len = 50
        self.screen = screen
        self.top_x = top_x
        self.top_y = top_y
        self.height = height
        self.width = width

    def render(self):
        draw_rect(self.screen, self.top_x, self.top_y, self.width, self.height, colors('grey'))
        draw_rect(self.screen, self.top_x, self.top_y, self.bar_len / 100 * self.width,
                  self.height, colors('white'))

    def update(self, scroll=None):
        mouse_pos = pg.mouse.get_pos()
        if self.top_x <= mouse_pos[0] <= self.top_x + self.width - 2:
            if self.top_y <= mouse_pos[1] <= self.top_y + self.height:
                if scroll:
                    self.bar_len += 5 * scroll
                    if self.bar_len > 100:
                        self.bar_len = 100
                    elif self.bar_len < 0:
                        self.bar_len = 0
                    self.render()
                else:
                    self.bar_len = ((mouse_pos[0] - self.top_x) / self.width) * 100
                    self.render()
                return self.bar_len
        return
