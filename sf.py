from pynput import keyboard
from threading import Thread
from datetime import datetime
import time
from window import get_active_application, focus_app
import sys

target_app_names = [
"RustDesk",
"Telegram",
"AnyDesk"
]


if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        target_app_names.append(sys.argv[i])

target_app_names = [ item.lower() for item in target_app_names ]

camou_app_name = 'Code'

period = 60
safe_window = ( 5, 4 )
warn_timestamp = datetime.now().timestamp() + period

is_risky = False
is_force_focused = False
hidden_app = None

def ensure_safety():
    global is_force_focused, hidden_app
    active_app = get_active_application()
    if active_app.lower() in target_app_names:
        hidden_app = active_app
        is_force_focused = True
        focus_app(camou_app_name)

def focus_back():
    global hidden_app, is_force_focused
    if is_force_focused:
        if hidden_app is not None:
            focus_app(hidden_app)
        is_force_focused = False
    print("---------")

def timer_thread_handler():
    global warn_timestamp, is_force_focused, is_risky
    while True:
        current_timestamp = datetime.now().timestamp()

        left = warn_timestamp - current_timestamp - safe_window[0]
        time.sleep(left)

        # Risky session
        is_risky = True
        print(datetime.now().timestamp())
        ensure_safety()
        while True:
            current_timestamp = datetime.now().timestamp()
            if current_timestamp >= warn_timestamp + safe_window[1]:
                break
            ensure_safety()
        is_risky = False
        # focus_back()

        warn_timestamp += period

timer_thread = Thread(target=timer_thread_handler)


seq_count = 0

def record_moment():
    global warn_timestamp
    print("s")
    warn_timestamp = datetime.now().timestamp() + period
    timer_thread.start()

def on_press(key):
    global seq_count, is_risky
    if key == keyboard.Key.caps_lock:
        seq_count += 1
        if seq_count == 2:
            record_moment()
            # seq_count = 0
    if key == keyboard.Key.alt_r:
        if not is_risky:
            focus_back()



with keyboard.Listener(on_press=on_press) as listener:
    print("Listening to autobid urls.")
    listener.join()