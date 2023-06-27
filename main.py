import os
from window import show_screenshare_window, selected_among_all_visible_windows

os.system("rm -rf scrshot/*")

window_info = selected_among_all_visible_windows()
show_screenshare_window(window_info)