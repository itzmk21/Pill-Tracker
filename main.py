import tkinter as tk
import tkinter.colorchooser
from datetime import datetime
from time import time
from tkinter.font import Font
from format_secs import FormattedSeconds
from notifications import Notification
import file_handling as file

win = tk.Tk()
menu = tk.Menu(win)
win.title('Pill Tracker')

DEFAULT_LIMIT: int = 13

STYLE: dict = {
    'DEFAULT_COLOURS': {
        'Grey-Black': '#202020',
        'Grey-White': '#D5D5D5',
        'Black': '#000000',
        'White': '#FFFFFF'
    },
    'DEFAULT_WIN_SIZE': {
        'DEFAULT_WIN_X': '900',
        'DEFAULT_WIN_Y': '800',
    },
    'RELIEF': 'solid',
    'PADX': '5',
    'PADY': '5',
    'BORDER': '1',
    'HEIGHT': '1',
    'FONT': Font
    (family='Segoe UI',
     size=15
     )
}

CONFIG_POS: dict = {
    'TIME_CONFIG': 0,
    'CONFIRM_CONFIG': 1,
    'NOTIFY_CONFIG': 2,
    'ACCENT1': 3,
    'ACCENT2': 4,
    'WINDOW_SIZE_X': 5,
    'WINDOW_SIZE_Y': 6
}

DEFAULT_WIN_SIZE: str = f'{STYLE["DEFAULT_WIN_SIZE"]["DEFAULT_WIN_X"]}x{STYLE["DEFAULT_WIN_SIZE"]["DEFAULT_WIN_Y"]}'
win.maxsize(int(win.winfo_screenwidth()), int(win.winfo_screenheight()))

try:
    config_: list = file.read_config()

    accent1 = config_[
        CONFIG_POS['ACCENT1']
    ]
    accent2 = config_[
        CONFIG_POS['ACCENT2']
    ]
    win.config(menu=menu,
               bg=accent1)
except:
    accent1, accent2 = STYLE['DEFAULT_COLOURS']['Grey-Black'], STYLE['DEFAULT_COLOURS']['White']
    win.config(menu=menu,
               bg=accent1)

try:
    config_: list = file.read_config()
    win.geometry(
        f'{config_[CONFIG_POS["WINDOW_SIZE_X"]]}'
        'x'
        f'{config_[CONFIG_POS["WINDOW_SIZE_Y"]]}')
except:
    win.geometry(DEFAULT_WIN_SIZE)


def limit_log() -> int:
    try:
        return int((int(file.read_config()[CONFIG_POS['WINDOW_SIZE_Y']]) / 80))
    except:
        return DEFAULT_LIMIT


label_ = tk.Label()
spaced_line, spaced_line2 = tk.Label(), tk.Label()

btn1, btn2, btn3, btn4, btn5, btn6 = tk.Button(), tk.Button(
), tk.Button(), tk.Button(), tk.Button(), tk.Button()

entry1, entry2 = tk.Button(), tk.Button()

time_frames_secs: dict = {
    'SECOND': 1,
    'MINUTE': 60,
    'HOUR': 3600,
    'DAY': 86400
}


def label(text) -> None:
    global label_
    destroy_last()
    label_ = tk.Label(text=text,
                      bg=accent1,
                      fg=accent2,
                      font=STYLE['FONT'])
    label_.pack()


def button(text, command, width='14', state=tk.NORMAL) -> tk.Button:
    return tk.Button(text=text,
                     relief=STYLE['RELIEF'],
                     bg=accent1,
                     fg=accent2,
                     activebackground=accent2,
                     activeforeground=accent1,
                     padx=STYLE['PADX'],
                     pady=STYLE['PADY'],
                     border=STYLE['BORDER'],
                     height=STYLE['HEIGHT'],
                     width=width,
                     font=STYLE['FONT'],
                     state=state,
                     command=command)


def themes_button(text, accent1_, accent2_, command, width='16') -> tk.Button:
    return tk.Button(text=text,
                     relief=STYLE['RELIEF'],
                     bg=accent1_,
                     fg=accent2_,
                     activebackground=accent2_,
                     activeforeground=accent1_,
                     padx=STYLE['PADX'],
                     pady=STYLE['PADY'],
                     border=STYLE['BORDER'],
                     height=STYLE['HEIGHT'],
                     width=width,
                     font=STYLE['FONT'],
                     command=command)


def entry(bg, fg) -> tk.Entry:
    return tk.Entry(bg=bg,
                    fg=fg,
                    border=STYLE['BORDER'],
                    width='14',
                    font=STYLE['FONT'])


def next_page_btn(state=tk.NORMAL) -> button:
    global btn1
    btn1 = button(text='Next Page',
                  state=state,
                  command=next_page)
    btn1.pack()


def previous_page_btn(state=tk.NORMAL) -> button:
    global btn2
    btn2 = button(text='Previous Page',
                  state=state,
                  command=previous_page)
    btn2.pack()


def date_time() -> label:
    label(text=f'{datetime.now().strftime("%d/%m/%y")}\n'
               f'{datetime.now().strftime("%I:%M %p")}')


def space_func() -> tk.Label:
    return tk.Label(text='',
                    bg=accent1)


def space() -> space_func:
    global spaced_line
    spaced_line = space_func()
    spaced_line.pack()


def space2() -> space_func:
    global spaced_line2
    spaced_line2 = space_func()
    spaced_line2.pack()


def confirm_back_btns(confirm_command, back_command) -> button:
    global btn1
    destroy_last()
    space()
    btn1 = button(text='Confirm',
                  command=confirm_command,
                  width='8')
    btn1.pack()

    back(back_command, width='8')


def back(back_command, width='14') -> button:
    global btn2
    btn2 = button(text='Go Back',
                  command=back_command,
                  width=width)
    btn2.pack()


def undo(undo_command) -> button:
    global btn6
    btn6 = button(text='Undo',
                  command=undo_command)
    btn6.pack()


def confirm_func(func):
    def wrapper(back_command):
        confirm_opt_config()
        confirm_back_btns(confirm_command=func,
                          back_command=back_command) if confirm_btn_config else func()

    return wrapper


def frequency_sec(duration) -> int:
    return time_frames_secs[duration]


def remember_time() -> None:
    global time_code, next_time

    config: list = file.read_config()
    time_code = config[CONFIG_POS['TIME_CONFIG']]

    frequency: int = frequency_sec('DAY')
    next_time = int(time_code) + frequency


def status(notification=True) -> None:
    global btn1
    try:
        remember_time()
        if round(time()) >= next_time:
            last_taken: str = FormattedSeconds(
                round(time()) - int(time_code)).return_formatted_secs()

            label(text=f'You have not taken your pill for today ({datetime.now().strftime("%d/%m/%y")}).\n'
                       f"The last time you've taken it was {last_taken} ago.")
            notify_opt_config()
            if notify_config and notification:
                Notification(title='You can take your pill for today!',
                             body=f'Last taken: {last_taken} ago.').phone()

        else:
            time_left_to_consume: str = FormattedSeconds(
                next_time - round(time())).return_formatted_secs()
            label(text=f'You have already taken your pill for today ({datetime.now().strftime("%d/%m/%y")}).\n'
                       f"Check back in {time_left_to_consume}.")
            notify_opt_config()
            if notify_config and notification:
                Notification(title='You\'ve already taken your pill!',
                             body=f'Check back in: {time_left_to_consume}.').phone()
        space()
        btn1 = button(text='Refresh',
                      command=lambda: status(notification=False))
        btn1.pack()
    except:
        label(
            text=f'You have not taken your pill for today ({datetime.now().strftime("%d/%m/%y")}). ')


def record_dose(again=' ', already=' ', caution=' ') -> None:
    global temp_config, btn1

    temp_config = file.read_config()
    file.handle_config(list_pos=CONFIG_POS['TIME_CONFIG'],
                       replacement=str(round(time())))

    with open(file.PATH_OF_LOG, 'a') as f:
        f.write(
            f'Taken{again}on: {datetime.now().strftime("%d/%m/%y")} @{datetime.now().strftime("%I:%M %p")}\n\n')
    label(
        text=f'You have{already}taken your pill for today '
             f'({datetime.now().strftime("%d/%m/%y")}).{caution}')

    space()
    undo(undo_command=undo_record)


@confirm_func
def record_log() -> None:
    try:
        remember_time()
        if round(time()) >= int(next_time):
            record_dose()
        else:
            record_dose(again=' (again) ',
                        already=' ALREADY ',
                        caution=' \nCAUTION! ')
    except:
        record_dose()


def undo_record() -> None:
    destroy_last()
    log: list = file.read_log()
    del log[-2]
    file.list_to_str_overwrite(file_name='log', list_name=log, joiner='\n\n')

    file.handle_config(list_pos=CONFIG_POS['TIME_CONFIG'],
                       replacement=f'{"TIME" if len(log) <= 1 else int(temp_config[CONFIG_POS["TIME_CONFIG"]])}')

    label(text='Record Undone.')


def read_log() -> None:
    global start_index, end_index, limit
    log: list = file.read_log()
    start_index, limit = 0, limit_log()

    if len(log) <= limit:
        end_index = len(log)
    else:
        end_index = limit

    log_content: str = '\n\n'.join(log[start_index:end_index])

    with open(file.PATH_OF_LOG) as f:
        label(text=f'{log_content}'
                   f'{"No Records Available." if f.read(1) != "T" else ""}')

    space()
    if len(log) > limit:
        next_page_btn()
    else:
        next_page_btn(state=tk.DISABLED)

    previous_page_btn(state=tk.DISABLED)


def next_page() -> None:
    global start_index, end_index, limit
    destroy_last()

    log: list = file.read_log()
    with open(file.PATH_OF_LOG) as f:
        log: str = f.read() + ('placeholder\n\n' *
                               ((round(len(log) / limit_log()) * limit_log()) - len(log)))
        log: list = log.split('\n\n')

    start_index += limit_log()
    limit += limit_log()

    if len(log) <= limit:
        end_index = len(log)
    else:
        end_index = limit

    log_content: str = '\n\n'.join(log[start_index:end_index])
    log_content: str = log_content.replace(
        'placeholder\n', '\n').replace('placeholder', '')

    label(text=f'{log_content}')
    space()

    if len(log) > limit:
        next_page_btn(state=tk.NORMAL)
    else:
        next_page_btn(state=tk.DISABLED)

    previous_page_btn()


def previous_page() -> None:
    global start_index, end_index, limit
    destroy_last()
    log: list = file.read_log()

    start_index -= limit_log()
    limit -= limit_log()

    if len(log) <= limit:
        end_index = len(log)
    else:
        end_index -= limit_log()

    log_content: str = '\n\n'.join(log[start_index:end_index])

    label(text=f'{log_content}')
    space()
    next_page_btn()

    if start_index != 0:
        previous_page_btn()
    else:
        previous_page_btn(state=tk.DISABLED)


@confirm_func
def reset() -> None:
    global accent1, accent2, temp_config, temp_log, btn1
    destroy_last()
    temp_config = file.read_config()
    temp_log = file.read_log()

    file.reset_txt(file_txt='config',
                   reset_text='TIME CONFIRM_CONFIG NOTIFY_CONFIG ACCENT1 ACCENT2 WINDOW_SIZE_X WINDOW_SIZE_Y')
    file.reset_txt(file_txt='log', reset_text='')

    accent1, accent2 = STYLE['DEFAULT_COLOURS']['Grey-Black'], STYLE['DEFAULT_COLOURS']['White']
    win.config(bg=accent1)
    win.geometry(DEFAULT_WIN_SIZE)

    label(text='Reset Successful.')
    space()
    undo(undo_command=undo_reset)


def undo_reset() -> None:
    global accent1, accent2
    destroy_last()

    file.list_to_str_overwrite(
        file_name='config', list_name=temp_config, joiner=' ')
    file.list_to_str_overwrite(
        file_name='log', list_name=temp_log, joiner='\n\n')

    try:
        accent1, accent2 = temp_config[CONFIG_POS['ACCENT1']
                                       ], temp_config[CONFIG_POS['ACCENT2']]
        win.config(bg=accent1)
    except:
        accent1, accent2 = STYLE['DEFAULT_COLOURS']['Grey-Black'], STYLE['DEFAULT_COLOURS']['White']
        win.config(bg=accent1)

    try:
        win.geometry(
            f'{temp_config[CONFIG_POS["WINDOW_SIZE_X"]]}x{temp_config[CONFIG_POS["WINDOW_SIZE_Y"]]}')
    except:
        win.geometry(DEFAULT_WIN_SIZE)

    label(text='Reset Undone.')


def quit_app() -> None:
    confirm_opt_config()
    confirm_back_btns(confirm_command=win.quit,
                      back_command=date_time) if confirm_btn_config else win.quit()


def settings_page(width='18') -> None:
    global btn1, btn2, btn3, btn4
    destroy_last()
    space()
    btn1 = button(text='Confirm Option',
                  width=width,
                  command=confirm_option)
    btn1.pack()

    btn2 = button(text='Push Notifications',
                  width=width,
                  command=notify_opt)
    btn2.pack()

    btn3 = button(text='Change Theme',
                  width=width,
                  command=themes)
    btn3.pack()

    btn4 = button(text='Change Window Size',
                  width=width,
                  command=change_win_x)
    btn4.pack()


def confirm_option() -> None:
    global btn1, btn3
    destroy_last()
    space()
    btn1 = button(text='Enable Confirm',
                  command=lambda: confirm_enabled(back_command=confirm_option))
    btn1.pack()

    btn3 = button(text='Disable Confirm',
                  command=lambda: confirm_disabled(back_command=confirm_option))
    btn3.pack()

    back(back_command=settings_page)


@confirm_func
def confirm_enabled() -> None:
    file.handle_config(list_pos=CONFIG_POS['CONFIRM_CONFIG'],
                       replacement='1')

    label(text='Confirm Enabled.')
    space()
    back(back_command=confirm_option)


@confirm_func
def confirm_disabled() -> None:
    file.handle_config(list_pos=CONFIG_POS['CONFIRM_CONFIG'],
                       replacement='0')

    label(text='Confirm Disabled.')
    space()
    back(back_command=confirm_option)


def confirm_opt_config() -> None:
    global confirm_btn_config
    config: list = file.read_config()
    try:
        if config[CONFIG_POS['CONFIRM_CONFIG']] == '0':
            confirm_btn_config = False
        else:
            confirm_btn_config = True
    except:
        confirm_btn_config = True


def notify_opt(width='23'):
    global btn1, btn3
    destroy_last()
    space()
    btn1 = button(text='Enable Push Notifications',
                  width=width,
                  command=lambda: notify_enabled(back_command=notify_opt))
    btn1.pack()

    btn3 = button(text='Disable Push Notifications',
                  width=width,
                  command=lambda: notify_disabled(back_command=notify_opt))
    btn3.pack()

    back(back_command=settings_page, width=width)


@confirm_func
def notify_enabled() -> None:
    file.handle_config(list_pos=CONFIG_POS['NOTIFY_CONFIG'],
                       replacement='1')

    label(text='Push Notifications Enabled.\nCheck your phone for the notification.')
    notify_opt_config()
    if notify_config:
        Notification(title='Notifications Option',
                     body='Notifications Enabled!').phone()
    space()
    back(back_command=notify_opt)


@confirm_func
def notify_disabled() -> None:
    file.handle_config(list_pos=CONFIG_POS['NOTIFY_CONFIG'],
                       replacement='0')

    label(text='Push Notifications Disabled.')
    Notification(title='Notifications Option',
                 body='Notifications Disabled!').phone()
    space()
    back(back_command=notify_opt)


def notify_opt_config() -> None:
    global notify_config
    config: list = file.read_config()
    try:
        if config[CONFIG_POS['NOTIFY_CONFIG']] == '0':
            notify_config = False
        else:
            notify_config = True
    except:
        notify_config = True


def themes() -> None:
    global btn1, btn3, btn4, btn5, btn6
    destroy_last()
    space()
    btn1 = themes_button(text='Dark Theme',
                         accent1_=STYLE['DEFAULT_COLOURS']['Grey-Black'],
                         accent2_=STYLE['DEFAULT_COLOURS']['White'],
                         command=lambda: dark_theme(back_command=themes))
    btn1.pack()

    btn3 = themes_button(text='Ultra Dark Theme',
                         accent1_=STYLE['DEFAULT_COLOURS']['Black'],
                         accent2_=STYLE['DEFAULT_COLOURS']['Grey-White'],
                         command=lambda: ultra_dark_theme(back_command=themes))
    btn3.pack()

    btn4 = themes_button(text='Light Theme',
                         accent1_=STYLE['DEFAULT_COLOURS']['White'],
                         accent2_=STYLE['DEFAULT_COLOURS']['Black'],
                         command=lambda: light_theme(back_command=themes))
    btn4.pack()

    btn5 = button(text='Custom Theme',
                  width='16',
                  command=custom_theme_accent1)
    btn5.pack()

    btn6 = themes_button(text='Switch Accent',
                         accent1_=accent2,
                         accent2_=accent1,
                         command=lambda: switch_accents(back_command=themes))
    btn6.pack()

    back(back_command=settings_page, width='16')


def set_theme(accent1_, accent2_, theme_type, back_command=themes) -> None:
    global accent1, accent2, btn1, temp_config
    temp_config = file.read_config()

    accent1, accent2 = accent1_, accent2_
    win.config(bg=accent1)

    file.handle_config(list_pos=CONFIG_POS['ACCENT1'],
                       replacement=accent1,
                       list_pos2=CONFIG_POS['ACCENT2'],
                       replacement2=accent2)

    label(text=f'{theme_type} Theme Enabled.')
    space()
    undo(undo_command=undo_theme)
    back(back_command=back_command)


def undo_theme() -> None:
    global accent1, accent2
    try:
        accent1, accent2 = temp_config[CONFIG_POS['ACCENT1']
                                       ], temp_config[CONFIG_POS['ACCENT2']]
        win.config(bg=accent1)
    except:
        accent1, accent2 = STYLE['DEFAULT_COLOURS']['Grey-Black'], STYLE['DEFAULT_COLOURS']['White']
        win.config(bg=accent1)

    file.handle_config(list_pos=CONFIG_POS['ACCENT1'],
                       replacement=accent1,
                       list_pos2=CONFIG_POS['ACCENT2'],
                       replacement2=accent2)

    label(text='Undone Theme.')
    space()
    back(back_command=themes)


@confirm_func
def dark_theme() -> None:
    set_theme(accent1_=STYLE['DEFAULT_COLOURS']['Grey-Black'],
              accent2_=STYLE['DEFAULT_COLOURS']['White'],
              theme_type='Dark')


@confirm_func
def ultra_dark_theme() -> None:
    set_theme(accent1_=STYLE['DEFAULT_COLOURS']['Black'],
              accent2_=STYLE['DEFAULT_COLOURS']['Grey-White'],
              theme_type='Ultra Dark')


@confirm_func
def light_theme() -> None:
    set_theme(accent1_=STYLE['DEFAULT_COLOURS']['White'],
              accent2_=STYLE['DEFAULT_COLOURS']['Black'],
              theme_type='Light')


@confirm_func
def switch_accents() -> None:
    set_theme(accent1_=accent2,
              accent2_=accent1,
              theme_type='Custom')


def colour_picker_accent1() -> None:
    global colour1
    colour1 = tk.colorchooser.Chooser().show()[1]
    try:
        entry1.insert(tk.END, string=colour1)
        custom_theme_accent2()
    except:
        pass


def colour_picker_accent2() -> None:
    global colour2
    colour2 = tk.colorchooser.Chooser().show()[1]
    try:
        entry2.insert(tk.END, string=colour2)
        confirm_custom_theme()
    except:
        pass


def custom_theme_accent1() -> None:
    global entry1, btn1, btn3

    label(text='Hex Code/Colour Name:')
    space()
    entry1 = entry(bg=accent1,
                   fg=accent2)
    entry1.bind('<Return>', custom_theme_accent2)
    entry1.pack()

    space2()
    btn1 = button(text='Enter Accent 1',
                  command=custom_theme_accent2)
    btn1.pack()

    btn3 = button(text='Colour Picker',
                  command=colour_picker_accent1)
    btn3.pack()

    back(back_command=themes)


def custom_theme_accent2(placeholder_for_entrybind=None) -> None:
    global entry2, btn1, btn3, colour1
    colour1 = entry1.get().replace(' ', '')
    destroy_last()

    label(text='Hex Code/Colour Name:')
    space()
    entry2 = entry(bg=accent1,
                   fg=accent2)
    entry2.bind('<Return>', confirm_custom_theme)
    entry2.pack()

    space2()
    btn1 = button(text='Enter Accent 2',
                  command=confirm_custom_theme)
    btn1.pack()

    btn3 = button(text='Colour Picker',
                  command=colour_picker_accent2)
    btn3.pack()

    back(back_command=custom_theme_accent1)


def set_custom_theme() -> None:
    try:
        try_lbl = tk.Label(text='',
                           bg=colour1,
                           fg=colour2)
        try_lbl.destroy()

        set_theme(accent1_=colour1,
                  accent2_=colour2,
                  theme_type='Custom')
    except:
        set_theme(accent1_=accent1,
                  accent2_=accent2,
                  theme_type='Invalid Colours. Previous',
                  back_command=custom_theme_accent1)


def confirm_custom_theme(placeholder_for_entrybind=None) -> None:
    global colour2
    colour2 = entry2.get().replace(' ', '')
    destroy_last()

    confirm_opt_config()
    confirm_back_btns(confirm_command=set_custom_theme,
                      back_command=custom_theme_accent1) if confirm_btn_config else set_custom_theme()


def change_win_x() -> None:
    global entry1, btn1, btn3

    def set_default_x() -> None:
        entry1.delete(0, tk.END)
        entry1.insert(0, STYLE['DEFAULT_WIN_SIZE']['DEFAULT_WIN_X'])
        change_win_y()

    label(text='Window Size [X] Value:')
    space()
    entry1 = entry(bg=accent1,
                   fg=accent2)
    entry1.bind('<Return>', change_win_y)
    entry1.pack()

    space2()
    btn1 = button(text='Enter [X] Value',
                  command=change_win_y)
    btn1.pack()

    btn3 = button(text='Default',
                  command=set_default_x)
    btn3.pack()

    back(back_command=settings_page)


def change_win_y(placeholder_for_entrybind=None) -> None:
    global entry2, btn1, btn3, winx_entry_var
    winx_entry_var = entry1.get().replace(' ', '')
    destroy_last()

    def set_default_y() -> None:
        entry2.delete(0, tk.END)
        entry2.insert(0, STYLE['DEFAULT_WIN_SIZE']['DEFAULT_WIN_Y'])
        confirm_change_win_size()

    label(text='Window Size [Y] Value:')
    space()
    entry2 = entry(bg=accent1,
                   fg=accent2)
    entry2.bind('<Return>', confirm_change_win_size)
    entry2.pack()

    space2()
    btn1 = button(text='Enter [Y] Value',
                  command=confirm_change_win_size)
    btn1.pack()

    btn3 = button(text='Default',
                  command=set_default_y)
    btn3.pack()

    back(back_command=change_win_x)


def set_win_size() -> None:
    global temp_config
    temp_config = file.read_config()
    try:
        win.geometry(f'{winx_entry_var}x{winy_entry_var}')

        file.handle_config(list_pos=CONFIG_POS['WINDOW_SIZE_X'],
                           replacement=winx_entry_var,
                           list_pos2=CONFIG_POS['WINDOW_SIZE_Y'],
                           replacement2=winy_entry_var)

        label(text='Window Size Change Successful.')
        space()
        undo(undo_command=undo_win_size)
        back(back_command=settings_page)
    except:
        label(text='Invalid Values. Previous Size Set.')
        space()
        back(back_command=change_win_x)


def confirm_change_win_size(placeholder_for_entrybind=None) -> None:
    global winy_entry_var
    winy_entry_var = entry2.get().replace(' ', '')
    destroy_last()

    confirm_opt_config()
    confirm_back_btns(confirm_command=set_win_size,
                      back_command=change_win_x) if confirm_btn_config else set_win_size()


def undo_win_size() -> None:
    global winx_entry_var, winy_entry_var
    winx_entry_var, winy_entry_var = temp_config[CONFIG_POS['WINDOW_SIZE_X']
                                                 ], temp_config[CONFIG_POS['WINDOW_SIZE_Y']]
    win.geometry(f'{winx_entry_var}x{winy_entry_var}')

    file.handle_config(list_pos=CONFIG_POS['WINDOW_SIZE_X'],
                       replacement=winx_entry_var,
                       list_pos2=CONFIG_POS['WINDOW_SIZE_Y'],
                       replacement2=winy_entry_var)

    label(text='Undone Window Size Change.')
    space()
    back(back_command=settings_page)


def read_config() -> None:
    config: list = file.read_config()
    label(text=f"'{config[CONFIG_POS['TIME_CONFIG']]}': Time Code (The last time you've taken your pill).\n\n"
               f"'{config[CONFIG_POS['CONFIRM_CONFIG']]}': Confirm Option ({'Disabled' if config[1] == '0' else 'Enabled'}).\n\n"
               f"'{config[CONFIG_POS['NOTIFY_CONFIG']]}': Push Notifications Option ({'Disabled' if config[2] == '0' else 'Enabled'}).\n\n"
               f"'{config[CONFIG_POS['ACCENT1']]}': Background Colour.\n\n"
               f"'{config[CONFIG_POS['ACCENT2']]}': Foreground Colour.\n\n"
               f"'{config[CONFIG_POS['WINDOW_SIZE_X']]}': Window's Size X.\n\n"
               f"'{config[CONFIG_POS['WINDOW_SIZE_Y']]}': Window's Size Y.")


def gui() -> None:
    main_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Main',
                     menu=main_menu)
    main_menu.add_command(label='Status',
                          command=status)
    main_menu.add_command(label='Log',
                          command=lambda: record_log(back_command=date_time))
    main_menu.add_command(label='Read Log',
                          command=read_log)

    admin_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label='Admin',
                     menu=admin_menu)
    admin_menu.add_command(label='Settings',
                           command=settings_page)
    admin_menu.add_command(label='Check Config',
                           command=read_config)
    admin_menu.add_command(label='Reset',
                           command=lambda: reset(back_command=date_time))
    admin_menu.add_command(label='Exits',
                           command=quit_app)

    tk.mainloop()


def destroy_last() -> None:
    label_.destroy()

    spaced_line.destroy()
    spaced_line2.destroy()

    btn1.destroy()
    btn2.destroy()
    btn3.destroy()
    btn4.destroy()
    btn5.destroy()
    btn6.destroy()

    entry1.destroy()
    entry2.destroy()


def run():
    date_time()
    gui()


if __name__ == '__main__':
    run()
