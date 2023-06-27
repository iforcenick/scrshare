from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll
from AppKit import NSWorkspace
from tkinter import *
import pyautogui
from screenshot import take_screenshot
from mask import set_mask, get_mask
import subprocess

def get_all_windows():
    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionAll, kCGNullWindowID)
    return window_list
def get_all_visible_windows():
    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionAll, kCGNullWindowID)
    windows = list(filter(lambda w: w.get('kCGWindowIsOnscreen', False), window_list))
    return windows

def get_all_visible_windows_with_priority():
    windows = []
    window_list = get_all_visible_windows()

    for window_index, window in enumerate(window_list):
        window_name = (window.get('kCGWindowName', ''))
        if window_name == "":
            continue
        window_id = window['kCGWindowNumber']
        owner_name = window['kCGWindowOwnerName']
        windows.append((window_id, window_name, owner_name))

    def get_priority(window):
        owner_name = window['kCGWindowOwnerName']
        owner_name = owner_name.lower()
        priorities = [ 'rustdesk', 'screen sharing', 'google chrome', 'zoom.us', 'microsoft teams' ]
        if owner_name in priorities:
            return "_" * (len(priorities) - priorities.index(owner_name)) + owner_name
        return owner_name
    window_list.sort(key=lambda x: get_priority(x))
    return windows

def query_window_by_owner_name(owner_name: str):
    window_list = get_all_visible_windows()
    return list(filter(lambda w: w['kCGWindowOwnerName'] == owner_name, window_list))

def query_window_by_pid(pid):
    window_list = get_all_visible_windows()
    return list(filter(lambda w: int(w['kCGWindowOwnerPID']) == pid, window_list))

def find_window_id(window_name):
    global windowId
    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionAll, kCGNullWindowID)

    for window in window_list:
        wn = (window.get('kCGWindowName', ''))
        if window_name == wn:
            return window['kCGWindowNumber']

    return None

def show_screenshare_window(window):
    (window_id, _, owner_name) = window
    screen_size = pyautogui.size()

    #Create an instance of tkinter frame
    win= Tk()

    mask = get_mask(owner_name)
    (img, _) = take_screenshot(window_id, mask=mask)
    canvas= Canvas(win, width=screen_size.width, height=screen_size.height)
    canvas.place(x=-3, y=-3)
    image_container = canvas.create_image(0,0, anchor="nw", image=img)


    def update_image():
        nonlocal canvas, win, image_container, window_id
        (img, _) = take_screenshot(window_id)
        win.geometry(f"{img.width() - 3}x{img.height() - 3}")
        canvas.imgref = img
        canvas.itemconfig(image_container,image=img)
        win.after(1, update_image)

    #Make the window borderless
    win.overrideredirect(True)
    win.after(1, update_image)
    win.mainloop()

def show_selection_window(windows):
    #Create an instance of tkinter frame
    win= Tk()
    win.geometry(f"1280x720")
    # win.title('Select the window th show')

    sidebar = Listbox(win, width=30, height=40)
    sidebar.grid(row=0, column=0, rowspan=2, padx=10, pady=5)
    mask_frame = Frame(win)
    mask_frame.grid(row=0, column=1, padx=10, pady=5)

    selected_window = None

    img_label = Label(win, image = None, text="Please select the window you want to share.")
    img_label.grid(row=1, column=1, padx=10, pady=5)

    def on_item_select(event):
        nonlocal selected_window
        selection = event.widget.curselection()
        img = None
        if selection is None or len(selection) == 0:
            return
        index = selection[0]
        window_id = window['kCGWindowNumber']
        selected_window = windows[index]

        (img, org_shape) = take_screenshot(window_id, (1024, 700))
        img_label.configure(image=img)
        img_label.image=img

    def on_double_click(event):
        print(event)
        win.destroy()

    for window_index, window in enumerate(windows):
        window_name = window.get('kCGWindowName', '')
        owner_name = window['kCGWindowOwnerName']
        sidebar.insert(window_index, f'{window_name} / {owner_name}')

    sidebar.bind('<<ListboxSelect>>', on_item_select)
    sidebar.bind('<Double-1>', on_double_click)
    #Define the size of the window or frame
    win.mainloop()
    return selected_window


def selected_among_all_visible_windows():
    windows = get_all_visible_windows_with_priority()
    return show_selection_window(windows)

def selected_owned_visible_window(owner_name):
    windows = query_window_by_owner_name(owner_name)
    if len(windows) == 0: return None
    if len(windows) == 1: return windows[0]
    return show_selection_window(windows)


def show_mask_area(selected_window):
    window_id, _, owner_name = selected_window

    win= Tk()
    win.geometry(f"1280x720")

    mask_frame = Frame(win)
    mask_frame.grid(row=0, column=1, padx=10, pady=5)

    def on_left_change(var):
        if selected_window is None: return
        owner_name = selected_window[2]
        mask = get_mask(owner_name)
        if mask is None: return
        try:
            mask[0] = int(var.get())
            set_mask(owner_name, mask)
        except:
            pass
    def on_right_change(var):
        if selected_window is None: return
        owner_name = selected_window[2]
        mask = get_mask(owner_name)
        if mask is None: return
        try:
            mask[1] = int(var.get())
            set_mask(owner_name, mask)
        except:
            pass
    def on_top_change(var):
        if selected_window is None: return
        owner_name = selected_window[2]
        mask = get_mask(owner_name)
        if mask is None: return
        try:
            mask[2] = int(var.get())
            set_mask(owner_name, mask)
        except:
            pass
    def on_bottom_change(var):
        if selected_window is None: return
        owner_name = selected_window[2]
        mask = get_mask(owner_name)
        if mask is None: return
        try:
            mask[3] = int(var.get())
            set_mask(owner_name, mask)
        except:
            pass

    left_var = StringVar()
    left_var.trace("w", lambda name, index, mode, var=left_var: on_left_change(var))
    right_var = StringVar()
    right_var.trace("w", lambda name, index, mode, var=right_var: on_right_change(var))
    top_var = StringVar()
    top_var.trace("w", lambda name, index, mode, var=top_var: on_top_change(var))
    bottom_var = StringVar()
    bottom_var.trace("w", lambda name, index, mode, var=bottom_var: on_bottom_change(var))

    left_input=Entry(mask_frame, width=6, textvariable=left_var)
    left_input.grid(row=0, column=0)
    right_input=Entry(mask_frame, width=6, textvariable=right_var)
    right_input.grid(row=0, column=1)
    top_input=Entry(mask_frame, width=6, textvariable=top_var)
    top_input.grid(row=0, column=2)
    bottom_input=Entry(mask_frame, width=6, textvariable=bottom_var)
    bottom_input.grid(row=0, column=3)

    if current_mask is None:
        current_mask = ( 0, 0, 0, 0 )
        set_mask(owner_name, current_mask)
    for mask_index, mask_input in enumerate(mask_entries):
        mask_input.delete(0, END)
        mask_input.insert(0, str(current_mask[mask_index]))

    mask_entries = [ left_input, right_input, top_input, bottom_input ]
    win.mainloop()
    return selected_window


def focus_app(app_name):
    cmd = f'osascript -e \'activate application "{app_name}"\''
    subprocess.call(cmd, shell=True)
    is_force_focused = True

def get_active_application():
    activeAppName = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    return activeAppName
