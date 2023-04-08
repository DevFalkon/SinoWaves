import pygame as pg
import sys
from pygame._sdl2.video import Window
from pygame import gfxdraw
import math
from ctypes import windll, wintypes, byref
import os

# To get the correct dimensions of the screen
user32 = windll.user32
user32.SetProcessDPIAware()


class Circle:
    def __init__(self, screen, centre_x, centre_y, rad, color) -> None:
        self.screen = screen
        # Drawing circle outline with antialiasing
        gfxdraw.aacircle(self.screen, centre_x, centre_y, rad, color)
        # Filling in the circle
        gfxdraw.filled_circle(self.screen, centre_x, centre_y, rad, color)
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.rad = rad

    def circle_dist(self, mouse_pos):  # Returns True is the cursor is inside the circle
        x_pos = mouse_pos[0] - self.centre_x
        y_pos = mouse_pos[1] - self.centre_y
        # Finding the distance of the cursor from the centre off the circle
        dist = math.sqrt(math.pow(x_pos, 2) + math.pow(y_pos, 2))
        if dist <= self.rad:
            return True
        return False


# To get the maximum possible size of a window
# total screen width, height-dock height
# also used to give the coordinates of top left corner of the screen
def get_max_window(max_width=True, origin=False):
    spi_get_work_area = 0x0030
    desktop_working_area = wintypes.RECT()

    _ = windll.user32.SystemParametersInfoW(spi_get_work_area, 0, byref(desktop_working_area), 0)

    left = int(str(desktop_working_area.left))
    right = int(str(desktop_working_area.right))
    top = int(str(desktop_working_area.top))
    bottom = int(str(desktop_working_area.bottom))
    if max_width:
        return right-left, bottom-top
    if origin:
        return left, top  # returns (x,y) position


# Returns the cursor position relative to the entire display
def get_abs_cursor_pos():
    cursor = wintypes.POINT()
    windll.user32.GetCursorPos(byref(cursor))
    return int(str(cursor.x)), int(str(cursor.y))  # Converts c_long to int


class GuiWindow:
    def __init__(self, width=1020, height=720, title="PygameGUI", logo=None):
        self.width, self.height = width, height
        self.title = title

        pg.init()
        self.screen = pg.display.set_mode((width, height), pg.NOFRAME)
        pg.display.set_caption(self.title)

        self.logo = logo
        if logo:
            icon = pg.image.load(logo).convert_alpha()
            pg.display.set_icon(icon)

        self.window = Window.from_display_module()
        self.top_bar_height = 35  # in px

        self.close_bttn = None
        self.min_bttn = None
        self.max_bttn = None

        self.screen_update = True
        self.is_out_of_screen = False
        self.title_bar()

        # variables for drag functionality
        self.drag_lock = False
        self.initial_window_position = get_max_window(max_width=False, origin=True)
        self.initial_mouse_position = (0, 0)
        self.relative_mouse_position = pg.mouse.get_pos()
        self.was_maximised = False

        # variables for maximising and minimising the app window
        self.last_position = self.window.position
        self.last_size = self.window.size
        self.is_maximised = False
        self.left_resize_lock = False
        self.bottom_resize_lock = False
        self.right_resize_lock = False
        self.initial_dimension = self.width, self.height

    # Run this method in every iteration of the main loop
    def win_update(self):
        left_click = pg.mouse.get_pressed()[0]
        mouse_pos = pg.mouse.get_pos()

        if self.close_bttn.circle_dist(mouse_pos) and not self.drag_lock:

            if left_click:
                self.quit_app()

        elif self.min_bttn.circle_dist(mouse_pos) and left_click and not self.drag_lock:
            pg.display.iconify()

        elif self.max_bttn.circle_dist(mouse_pos) and not self.drag_lock:
            self.drag_lock = True
            if left_click:
                if not self.is_maximised:
                    self.maximise()

                else:
                    self.minimise()

        self.drag_window(mouse_pos, left_click)
        if self.window.position[0] < 0:
            self.is_out_of_screen = True
        if self.window.size[0] + self.window.position[0] > get_max_window()[0]:
            self.is_out_of_screen = True

        if self.is_out_of_screen and self.window.position[0] > 0 and \
                self.window.size[0] + self.window.position[0] < get_max_window()[0]:
            self.is_out_of_screen = False
            pg.display.flip()
            self.title_bar()
            self.screen_update = True
        if left_click and mouse_pos[1] > self.top_bar_height:
            if self.drag_lock and not self.is_maximised:
                if self.width >= 1000 and self.height >= 700:
                    self.manual_resize(mouse_pos)
                if self.left_resize_lock or self.bottom_resize_lock or self.right_resize_lock:
                    if self.width < 1000:
                        self.width = 1000
                        self.window.size = self.width, self.height
                    if self.height < 700:
                        self.height = 700
                        self.window.size = self.width, self.height
                    self.screen_update = True
        else:
            self.initial_dimension = self.width, self.height
            if not pg.mouse.get_pressed()[0]:
                self.left_resize_lock = False
                self.bottom_resize_lock = False
                self.right_resize_lock = False

    def drag_window(self, mouse_pos, click):
        mouse_x, mouse_y = mouse_pos
        if not click or self.was_maximised:

            # Maximise the window if its y position is < -10
            pos_x, pos_y = self.window.position
            if pos_y < -5:
                pos_y = 0
                if pos_x < 0:
                    pos_x = 0
                self.window.position = pos_x, pos_y
                self.maximise()

            self.drag_lock = False
            self.was_maximised = False
            self.initial_mouse_position = get_abs_cursor_pos()
            self.relative_mouse_position = pg.mouse.get_pos()
            self.initial_window_position = self.window.position

        if mouse_y <= self.top_bar_height and mouse_x <= self.width - 90:

            if click and not self.drag_lock:

                if not self.is_maximised:
                    pos_x = self.initial_window_position[0] - \
                            (self.initial_window_position[0] - get_abs_cursor_pos()[0]) - self.relative_mouse_position[
                                0]
                    pos_y = self.initial_window_position[1] - \
                            (self.initial_window_position[1] - get_abs_cursor_pos()[1]) - self.relative_mouse_position[
                                1]

                    if pos_y < -15:
                        pos_y = -15
                    self.window.position = pos_x, pos_y

                elif mouse_x <= self.width - 90:  # Minimising the window if dragged in full screen mode
                    self.minimise()
                    self.window.position = get_abs_cursor_pos()[0] - self.width // 2, 0
                    self.initial_window_position = self.window.position
                    self.drag_lock = True
                    self.was_maximised = True

        else:
            if click:
                self.drag_lock = True

    def centre_window(self):  # To centre the pygame window
        max_width, max_height = get_max_window()
        pos_x = max_width // 2 - self.width // 2
        pos_y = max_height // 2 - self.height // 2
        self.window.position = (pos_x, pos_y)

    def maximise(self):
        self.screen_update = True
        self.last_position = self.window.position
        self.last_size = self.width, self.height
        self.is_maximised = True

        self.width, self.height = get_max_window()
        self.window.size = self.width, self.height
        self.window.position = get_max_window(max_width=False, origin=True)
        pg.display.flip()
        self.title_bar()

    def minimise(self):
        self.screen_update = True
        self.is_maximised = False

        self.width, self.height = self.last_size
        self.window.size = self.width, self.height
        self.window.position = self.last_position
        pg.display.flip()
        self.title_bar()

    def manual_resize(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        border = 10
        if mouse_x <= border or self.left_resize_lock:
            if not (self.right_resize_lock or self.bottom_resize_lock):
                if not self.left_resize_lock:
                    self.initial_mouse_position = get_abs_cursor_pos()
                    self.left_resize_lock = True
                else:
                    final_pos = get_abs_cursor_pos()
                    width_add = final_pos[0] - self.initial_mouse_position[0]
                    self.width, self.height = self.initial_dimension[0] - width_add, self.height
                    self.window.position = self.initial_window_position[0] + width_add, self.initial_window_position[1]
                    self.window.size = self.width, self.height
                    pg.display.flip()
                    self.title_bar()

        if self.height - border <= mouse_y or self.bottom_resize_lock:
            if not (self.left_resize_lock or self.right_resize_lock):
                if not self.bottom_resize_lock:
                    self.initial_mouse_position = get_abs_cursor_pos()
                    self.bottom_resize_lock = True
                else:
                    final_pos = get_abs_cursor_pos()
                    height_add = final_pos[1] - self.initial_mouse_position[1]
                    self.width, self.height = self.width, self.initial_dimension[1] + height_add
                    self.window.size = self.width, self.height
                    pg.display.flip()
                    self.title_bar()

        if self.width - border <= mouse_x or self.right_resize_lock:
            if not (self.left_resize_lock or self.bottom_resize_lock):
                if not self.right_resize_lock:
                    self.initial_mouse_position = get_abs_cursor_pos()
                    self.right_resize_lock = True
                else:
                    final_pos = get_abs_cursor_pos()
                    width_add = final_pos[0] - self.initial_mouse_position[0]
                    self.width, self.height = self.initial_dimension[0] + width_add, self.height
                    self.window.size = self.width, self.height
                    pg.display.flip()
                    self.title_bar()

    def title_bar(self, color='grey'):
        title_bar_color = self.color(color)
        pg.draw.rect(self.screen, title_bar_color, pg.Rect(0, 0, self.width, self.top_bar_height))

        if self.title:
            title_size = self.top_bar_height - 15
            font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', title_size)
            text = font.render(self.title, True, self.color('white'))
            text_width = text.get_width()
            self.screen.blit(text, (self.width // 2 - text_width // 2, 5))

        if self.logo:
            icon = pg.image.load(self.logo).convert_alpha()
            icon = pg.transform.smoothscale(icon, (self.top_bar_height - 5, self.top_bar_height - 5))
            self.screen.blit(icon, (10, 2))

        self.close_bttn = Circle(self.screen, self.width - 25,
                                 self.top_bar_height // 2,
                                 self.top_bar_height // 4,
                                 self.color('red'))
        self.max_bttn = Circle(self.screen, self.width - 50,
                               self.top_bar_height // 2,
                               self.top_bar_height // 4,
                               self.color('yellow'))
        self.min_bttn = Circle(self.screen, self.width - 75,
                               self.top_bar_height // 2,
                               self.top_bar_height // 4,
                               self.color('green'))

        pg.display.update(pg.Rect(0, 0, self.width, self.top_bar_height))

    @staticmethod
    def color(color):
        colors = {
            'red': (235, 18, 7),
            'green': (74, 222, 16),
            'yellow': (235, 200, 7),
            'grey': (61, 61, 61),
            'light_grey': (163, 160, 158),
            'white': (255, 255, 255),
            'dark_grey': (41, 41, 41)
        }
        return colors[color]

    def quit_app(self):
        # Closing animation
        opacity = self.window.opacity * 100
        while opacity > 0:
            opacity -= 20
            self.window.opacity = opacity / 100
            pg.time.Clock().tick(100)

        # Closing the app
        pg.quit()
        sys.exit()
