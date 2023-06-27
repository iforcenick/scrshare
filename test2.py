from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionAll


def get_all_windows():
    windows = []
    window_list = CGWindowListCopyWindowInfo(
        kCGWindowListOptionAll, kCGNullWindowID)
    for window_index, window in enumerate(window_list):
        if window["kCGWindowOwnerName"] != "Mattermost":
            continue
        print(window)
        window_name = (window.get('kCGWindowName', ''))
        if window_name == "":
            continue
        window_id = window['kCGWindowNumber']
        owner_name = window['kCGWindowOwnerName']
        windows.append((window_id, window_name, owner_name))

    def get_priority(owner_name: str):
        owner_name = owner_name.lower()
        priorities = [ 'rustdesk', 'screen sharing', 'google chrome', 'zoom.us', 'microsoft teams' ]
        if owner_name in priorities:
            return "_" * (len(priorities) - priorities.index(owner_name)) + owner_name
        return owner_name
    windows.sort(key=lambda x: get_priority(x[2]))
    return windows

get_all_windows()