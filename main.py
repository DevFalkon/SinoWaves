import os
import pygame as pg
import modules.PygameGUI as PygameGUI
from modules.PygameGUI import widgets
import modules.PyMusic as PyMusic
import modules.PlayerHandler as PlayerHandler
from threading import Thread
import subprocess

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
iterable_content = "downloads"
iterable = []
recently_played = widgets.Button(screen, 0, 0, 10, 10, 10, widgets.colors('white'))
downloads = widgets.Button(screen, 0, 0, 10, 10, 10, widgets.colors('white'))
download_sng = widgets.Button(screen, 0, 0, 10, 10, 10, widgets.colors('white'))

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


def check_for_updates():
    import urllib.request
    import re

    for i in os.listdir():
        if i == 'del':
            subprocess.run("rmdir /s /Q del", shell=True)
            break

    try:
        html = urllib.request.urlopen(f"https://github.com/DevFalkon/SinoWaves/releases")
        versions = re.findall(r"href=\"/DevFalkon/SinoWaves/releases/tag/v(\S{5})\"", html.read().decode())
        highest_version = ''.join(versions[0].split('.'))
        with open('version.txt', 'r') as file:
            data = file.read()[1::]
        data = ''.join(data.split('.'))
        return (highest_version > data)
    except:
        return False


def update_scroll_header(text):
    font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', size=height // 16)
    widgets.draw_rect(screen, 3 * column_spacing + int(col_r[0] * width) + 10,
                      y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 112 - height // 16,
                      int(col_r[1] * width) - 2 * column_spacing - 24,
                      height // 16 + 20, widgets.colors('dark_grey'))
    text = font.render(text.capitalize(), True, widgets.colors('white'))
    screen.blit(text, (3 * column_spacing + int(col_r[0] * width) + 10,
                       y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 112 - height // 16))
    pg.display.update(pg.Rect(3 * column_spacing + int(col_r[0] * width) + 10,
                              y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 112 - height // 16,
                              int(col_r[1] * width) - 2 * column_spacing - 24,
                              height // 16 + 20))


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
    text = ''
    if iterable_content == "downloads":
        text = "downloads"
    elif iterable_content == "recent":
        text = "recently played"
    update_scroll_header(text)
    pg.display.update(pg.Rect(3 * column_spacing + int(col_r[0] * width) + 10,
                              y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 122 - height // 16,
                              int(col_r[1] * width) - 5 * column_spacing, height // 16 + 10))
    widgets.draw_rect(screen, 3 * column_spacing + int(col_r[0] * width),
                      y_coord_0 + 2 * row_spacing + int(height * row_r[0]) + 132,
                      int(col_r[1] * width) - 4 * column_spacing, 4, widgets.colors('white'))
    global main_scroll
    save_iter = main_scroll.iterable
    if not save_iter:
        if iterable_content == "downloads":
            save_iter = load_saved_songs()
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

    button_height = int(row_r[1] * height) // 16
    sch_bar_height = search_bar.height
    global downloads
    downloads = widgets.Button(screen, column_spacing + 5, y_coord_0 + 2*row_spacing + sch_bar_height,
                               int(col_r[0] * width) - 10, button_height, menu_radius-10,
                               widgets.colors('dark_grey'),
                               text="Downloads", bg_col="blue_1")
    global recently_played
    recently_played = widgets.Button(screen, column_spacing + 5,
                                     y_coord_0 + 2*row_spacing + height//300 + button_height + sch_bar_height,
                                     int(col_r[0] * width) - 10, button_height, menu_radius-10,
                                     widgets.colors('dark_grey'),
                                     text="Recently Played", bg_col="blue_1")

    global download_sng
    download_sng = widgets.Button(screen, width // 2 + 4 * (height - 50) // 22 + 5,
                                  int(height * (1 - row_r[2]) + 6 * row_spacing +
                                      height // 65 + button_height//4),
                                  int(col_r[0] * width) - 10, button_height,
                                  menu_radius-10, widgets.colors('dark_grey'),
                                  text="Download Song", bg_col="blue_1")


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
        os.mkdir('saved\\music')

    dat = []
    for file in os.listdir('saved\\music'):
        file = file[:-4]
        dat.append(file)

    return dat


def load_recent_songs():
    dat = []
    for file in os.listdir('saved\\temp'):
        file = file[:-4]
        dat.append(file)

    return dat


yes_upd = None
no_upd = None

def update_window():
    wd = width//2
    ht = height//2
    widgets.draw_rect(screen, width//2-wd//2, height//2-ht//2, wd, ht, widgets.colors('light_grey'))
    font = pg.font.Font('modules\\PygameGUI\\fonts\\Inter-Regular.ttf', size=height // 16)
    text = "update available"
    text = font.render(text.capitalize(), True, widgets.colors('black'))
    screen.blit(text, (width//2-wd//4, height//2-ht//2))
    pg.display.update(width//2-wd//2, height//2-ht//2, wd, ht)
    global yes_upd, no_upd
    yes_upd = widgets.Button(screen, width//2 - wd//2 + 10, height//2 + ht//2 - ht//10 - 10,
                             wd//2 - 20, ht//10, 15, widgets.colors('black'),
                             text="Update Now", bg_col="light_grey")
    no_upd = widgets.Button(screen, width//2 + 10, height//2 + ht//2 - ht//10 - 10,
                            wd//2 - 20, ht//10, 15, widgets.colors('black'),
                            text="Update Later", bg_col="light_grey")


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
current_sng_name = None
min_check = False
update = False
if check_for_updates():
    update = True


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

    if not pg.display.get_active():
        min_check = True

    if min_check and pg.display.get_active():
        min_check = False
        app.screen_update = True

    if app.screen_update:
        pg.display.set_mode((app.width, app.height), pg.NOFRAME)
        screen_update()
        if update:
            update_window()

    if update:
        search_bar.is_active = False

    if current_sng_name and pg.mixer.music.get_pos() == -1 and len(iterable) > 1:
        ind = iterable.index(current_sng_name)
        if ind == len(iterable)-1:
            ind = 0
        else:
            ind += 1
        current_sng_name = iterable[ind]
        MusicPlayer.change_song(current_sng_name)
        control_buttons.play = True
        control_buttons.update(screen, width, height, row_r, row_spacing)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            app.quit_app()

        if event.type == pg.KEYDOWN:
            if search_bar.is_active:
                if search_bar.text != '':
                    if event.key == pg.K_RETURN:
                        iterable_content = "search"
                        th = Thread(target=search_for_sng)
                        th.start()
                        temp_sng_name = search_bar.text
                        got_search_res = False
                search_bar.type(event.key)
        if event.type == pg.MOUSEWHEEL and not update:
            if event.y:
                main_scroll.update(ev=event.y)

        if event.type == pg.MOUSEBUTTONDOWN:
            if not update:
                if event.button == 1:
                    if download_sng.get_pressed(pg.mouse.get_pos()) and MusicPlayer.song \
                            and not PyMusic.installing:
                        if f"{MusicPlayer.song}.mp3" not in os.listdir("saved\\music"):
                            th = Thread(target=PyMusic.convert, args=(MusicPlayer.song,))
                            th.start()

                    if downloads.get_pressed(pg.mouse.get_pos()):
                        if iterable_content != "downloads":
                            update_scroll_header("downloads")
                            iterable_content = "downloads"
                            iterable = load_saved_songs()
                            main_scroll.iterable = iterable
                            main_scroll.force_update()
                    if recently_played.get_pressed(pg.mouse.get_pos()):
                        if iterable_content != "recent":
                            update_scroll_header("recently played")
                            iterable_content = "recent"
                            iterable = load_recent_songs()
                            main_scroll.iterable = iterable
                            main_scroll.force_update()

                    if temp_sng_name or current_sng_name:
                        if pg.mixer.music.get_pos() != -1:
                            control_buttons.pause_play(screen, width, height, row_r, row_spacing)
                        forward = control_buttons.forward(screen, width, height, row_r, row_spacing)
                        if forward:
                            ind = iterable.index(current_sng_name)
                            if ind == len(iterable)-1:
                                ind = 0
                            else:
                                ind += 1
                            current_sng_name = iterable[ind]
                            MusicPlayer.change_song(current_sng_name)
                        back = control_buttons.back(screen, width, height, row_r, row_spacing)
                        if back:
                            ind = iterable.index(current_sng_name)
                            if ind == 0:
                                ind = len(iterable)-1
                            else:
                                ind -= 1
                            current_sng_name = iterable[ind]
                            MusicPlayer.change_song(current_sng_name)

                    elem = main_scroll.get_name()

                    if iterable_content == "downloads":
                        if elem:
                            current_sng_name = elem
                            control_buttons.play = True
                            control_buttons.update(screen, width, height, row_r, row_spacing)
                            MusicPlayer.change_song(elem)
                            temp_sng_name = None
                    elif iterable_content == "recent":
                        if elem:
                            temp_sng_name = elem
                            control_buttons.play = True
                            control_buttons.update(screen, width, height, row_r, row_spacing)
                            MusicPlayer.change_song(elem, temp=True)
                            current_sng_name = None
                    else:
                        if elem:
                            if not PyMusic.curr_ints:
                                th = Thread(target=PyMusic.inst, args=(elem, temp_sng_name))
                                th.start()
            else:
                if event.button == 1:
                    if yes_upd.get_pressed(pg.mouse.get_pos()):
                        subprocess.Popen(["python", "update.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)
                        app.quit_app()
                    if no_upd.get_pressed(pg.mouse.get_pos()):
                        update = False
                        pg.display.set_mode((app.width, app.height), pg.NOFRAME)
                        screen_update()

    clock.tick(FPS)
