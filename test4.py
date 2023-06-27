import subprocess

camou_app_name = "RustDesk"

app_name = camou_app_name
cmd = f'osascript -e \'activate application "{app_name}"\''
subprocess.call(cmd, shell=True)