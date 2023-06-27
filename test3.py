from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll

def get_all_visible_windows():
    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionAll, kCGNullWindowID)
    windows = list(filter(lambda w: w.get('kCGWindowIsOnscreen', False), window_list))
    return windows

windows = get_all_visible_windows()
window_h = 'RustDesk'
window_c = 'OpenVPN Connect'

for window_index, window in enumerate(windows):
    owner_name = window['kCGWindowOwnerName']
    window_id = window['kCGWindowNumber']
    print(owner_name)
