import os
import pygame as pg
import modules.PygameGUI as PygameGUI
from modules.PygameGUI import widgets
import modules.PyMusic as PyMusic
import modules.PlayerHandler as PlayerHandler
from threading import Thread

icon = 'graphics//icon.png'
app = PygameGUI.GuiWindow(logo=icon)
app.title = "Sino Waves"
pg.display.set_caption(app.title)
app.maximise()
screen = app.screen

clock = pg.time.Clock()
FPS = 100

col_r = [0.15, 0.55, 0.30]
row_r = [0.065, 0.85, 0.15]
column_spacing = 10
row_spacing = 10
menu_radius = 25

y_coord_0 = app.top_bar_height
height = app.height - app.top_bar_height
width = app.width
iterable_content = "Downloads"
iterable = []


main_scroll = widgets.Scroll(screen, 3 * column_spacing + int(col_r[0] * width),
                             y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 152,
                             int(col_r[1] * width) - 4 * column_spacing,
                             int(height * (row_r[1] - row_r[0])) - 3 * row_spacing - 162,
                             iterable,
                             height)


song_progress_bar = widgets.PlayerProgressBar(screen,
                                              40,
                                              int(height * (1 - row_r[2])) + 5 * row_spacing,
                                              width - 80, height // 65)

search_bar = widgets.SearchBar(screen, 2 * column_spacing + int(col_r[0] * width),
                               y_coord_0 + row_spacing,
                               int(col_r[1] * width) - 2 * column_spacing, int(height * row_r[0]))


def main_scroll_elements(surface):
    # Song list background
    widgets.rounded_rect(surface, 2 * column_spacing + int(col_r[0] * width),
                         y_coord_0 + 2 * row_spacing + int(height * row_r[0]),  # top y coordinate
                         int(col_r[1] * width) - 2 * column_spacing,  # Width
                         int(height * (row_r[1] - row_r[0])) - 3 * row_spacing,
                         menu_radius, widgets.colors('white'))

    widgets.rounded_rect(surface, 2 * column_spacing + int(col_r[0] * width) + 2,
                         y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 2,
                         int(col_r[1] * width) - 2 * column_spacing - 4,
                         int(height * (row_r[1] - row_r[0])) - 3 * row_spacing - 4,
                         menu_radius,
                         widgets.colors('dark_grey'), None)
    font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', size=height // 16)
    text = font.render(iterable_content, True, widgets.colors('white'))
    screen.blit(text, (3 * column_spacing + int(col_r[0] * width) + 10,
                       y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 112 - height // 16))
    pg.display.update(pg.Rect(3 * column_spacing + int(col_r[0] * width) + 10,
                              y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 122 - height // 16,
                              int(col_r[1] * width) - 5 * column_spacing, height // 16 + 10))
    widgets.draw_rect(screen, 3 * column_spacing + int(col_r[0] * width),
                      y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 132,
                      int(col_r[1] * width) - 4 * column_spacing, 4, widgets.colors('white'))
    global main_scroll
    save_iter = main_scroll.iterable
    main_scroll = widgets.Scroll(screen, 3 * column_spacing + int(col_r[0] * width),
                                 y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 135,
                                 int(col_r[1] * width) - 4 * column_spacing,
                                 int(height * (row_r[1] - row_r[0])) - 3 * row_spacing - 145,
                                 iterable,
                                 height)
    main_scroll.iterable = save_iter
    main_scroll.force_update()


def main_page_layout(surface):
    # Filling in the background
    widgets.draw_rect(surface, 0, y_coord_0, width, height, widgets.colors('dark_grey'))

    # Left menu bar background
    widgets.rounded_rect(surface, column_spacing,
                         y_coord_0 + row_spacing,
                         int(col_r[0] * width),
                         int(height * row_r[1]) - 2 * row_spacing,
                         menu_radius, widgets.colors('blue_1'))

    # Background for showing current processes
    widgets.rounded_rect(surface, column_spacing + int((col_r[0] + col_r[1]) * width),
                         y_coord_0 + 2 * row_spacing + int(height * row_r[0]),  # top y coordinate
                         int(col_r[2] * width) - 2 * column_spacing,  # Width
                         int(height * (row_r[1] - row_r[0])) - 3 * row_spacing,
                         menu_radius, widgets.colors('white'))

    widgets.rounded_rect(surface, column_spacing + int((col_r[0] + col_r[1]) * width) + 2,
                         y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 2,
                         int(col_r[2] * width) - 2 * column_spacing - 4,
                         int(height * (row_r[1] - row_r[0])) - 3 * row_spacing - 4,
                         menu_radius,
                         widgets.colors('dark_grey'), None)

    # Music player background
    widgets.rounded_rect(surface, column_spacing,
                         y_coord_0 + int(height * row_r[1]),
                         width - 2 * column_spacing,
                         int(height * row_r[2]) - row_spacing, menu_radius,
                         widgets.colors('blue_1'))

    main_scroll_elements(surface)

    global search_bar
    search_bar = widgets.SearchBar(surface, 2 * column_spacing + int(col_r[0] * width),
                                   y_coord_0 + row_spacing,
                                   int(col_r[1] * width) - 2 * column_spacing, int(height * row_r[0]))

    global song_progress_bar
    song_progress_bar.width = width - 80
    song_progress_bar.height = height // 65
    song_progress_bar.top_y = int(height * (1 - row_r[2])) + 5 * row_spacing
    song_progress_bar.render_bg()


def screen_update():
    global y_coord_0, height, width, main_scroll
    y_coord_0 = app.top_bar_height
    height = app.height - app.top_bar_height
    width = app.width
    app.title_bar()
    main_page_layout(screen)
    app.screen_update = False
    control_buttons.update(screen, width, height, row_r, row_spacing)


def load_saved_songs():
    for directory in os.listdir():
        if directory == 'saved':
            break
    else:
        os.mkdir('saved')
        os.mkdir('saved\\temp')
        os.mkdir('saved\\icon')
        os.mkdir('saved\\music')

    dat = []
    for file in os.listdir('saved\\music'):
        file = file[:-4]
        dat.append(file)

    return dat


got_search_res = True


def search_for_sng(run=True):
    global iterable_content, iterable, main_scroll
    if run:
        main_scroll.iterable = []
        thread = Thread(target=PyMusic.web_scraper, args=(search_bar.text,))
        thread.start()
        iterable_content = f'Results for: {search_bar.text}'

    if PyMusic.video_id:
        main_scroll.iterable = PyMusic.video_id
        PyMusic.video_id = []
        widgets.draw_rect(screen, 3 * column_spacing + int(col_r[0] * width) + 10,
                          y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 122 - height // 16,
                          int(col_r[1] * width) - 5 * column_spacing, height // 16 + 10,
                          widgets.colors('dark_grey'))
        font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', size=height // 16)
        text = font.render(iterable_content, True, widgets.colors('white'))
        screen.blit(text, (3 * column_spacing + int(col_r[0] * width) + 10,
                           y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 112 - height // 16))
        pg.display.update(pg.Rect(3 * column_spacing + int(col_r[0] * width) + 10,
                                  y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 122 - height // 16,
                                  int(col_r[1] * width) - 5 * column_spacing, height // 16 + 10))
        main_scroll.scroll = 0
        main_scroll.force_update()
        global got_search_res
        got_search_res = True

    search_bar.text = ''
    search_bar.is_active = False


iterable = load_saved_songs()
MusicPlayer = PlayerHandler.Player(song_progress_bar)
control_buttons = PlayerHandler.MusicControlButtons()
temp_sng_name = None


while 1:

    app.win_update()

    MusicPlayer.update_bar()
    search_bar.activate(pg.mouse.get_pos(), pg.mouse.get_pressed()[0])

    if not got_search_res:
        search_for_sng(run=False)

    if PyMusic.is_temp_playing:
        MusicPlayer.change_song(PyMusic.temp_sng, temp=True)
        PyMusic.is_temp_playing = False
        control_buttons.play = True
        control_buttons.update(screen, width, height, row_r, row_spacing)

    if not pg.mixer.music.get_busy() and control_buttons.play:
        control_buttons.play = False
        control_buttons.update(screen, width, height, row_r, row_spacing)

    if app.screen_update or not pg.display.get_active():
        screen_update()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            app.quit_app()

        if event.type == pg.KEYDOWN:
            if search_bar.is_active:
                if search_bar.text != '':
                    if event.key == pg.K_RETURN:
                        th = Thread(target=search_for_sng)
                        th.start()
                        temp_sng_name = search_bar.text
                        got_search_res = False
                search_bar.type(event.key)

        if event.type == pg.MOUSEWHEEL:
            if event.y:
                main_scroll.update(ev=event.y)

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:

                if temp_sng_name:
                    control_buttons.pause_play(screen, width, height, row_r, row_spacing)
                    forward = control_buttons.forward(screen, width, height, row_r, row_spacing)
                    back = control_buttons.back(screen, width, height, row_r, row_spacing)

                elem = main_scroll.get_name()
                if iterable_content == "Downloads":
                    if elem:
                        MusicPlayer.change_song(elem)
                else:
                    if elem:
                        if not PyMusic.curr_ints:
                            th = Thread(target=PyMusic.inst, args=(elem, temp_sng_name))
                            th.start()

    clock.tick(FPS)
