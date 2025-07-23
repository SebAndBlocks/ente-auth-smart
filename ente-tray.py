import threading
import subprocess
import sys
import os
import json
from flask import Flask, jsonify
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox
import base64
from io import BytesIO

PORT = 8765

# Config path for Windows and Linux only
if sys.platform == "win32":
    CONFIG_PATH = r"C:\ProgramData\ente-tray\config.json"
else:  # assume linux
    CONFIG_PATH = "/etc/ente-tray/config.json"

# Default Ente Auth executable paths for Windows and Linux only
DEFAULT_PATHS = {
    "win32": r"C:\Program Files\Ente Auth\auth.exe",
    "linux": "/usr/local/bin/ente-auth",
}

app = Flask(__name__)

def show_error(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ente Tray Error", message)
    root.destroy()

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                exe_path = data.get("ente_auth_executable")
                if exe_path and os.path.isfile(exe_path):
                    return exe_path
        except Exception as e:
            print(f"Failed to load config file: {e}")
    return None

def find_ente_auth_executable():
    platform_key = sys.platform
    if platform_key.startswith("linux"):
        platform_key = "linux"  # normalize

    # 1. Try config file path first
    exe_path = load_config()
    if exe_path:
        return exe_path

    # 2. Try platform default path
    default_path = DEFAULT_PATHS.get(platform_key)
    if default_path and os.path.isfile(default_path):
        return default_path

    # 3. Not found, show error dialog and exit
    msg = (
        f"Cannot find Ente Auth executable.\n\n"
        f"Please create a config file with the following format:\n"
        f"{CONFIG_PATH}\n\n"
        f'{{\n  "ente_auth_executable": "full_path_to_EnteAuth_executable"\n}}'
    )
    show_error(msg)
    sys.exit(1)

ENTE_AUTH_CMD = [find_ente_auth_executable()]

def launch_ente_auth():
    try:
        subprocess.Popen(ENTE_AUTH_CMD)
        print("Ente Auth launched.")
    except Exception as e:
        print(f"Failed to launch Ente Auth: {e}")

@app.route('/popup', methods=['GET'])
def popup():
    launch_ente_auth()
    return jsonify({"status": "Ente Auth popup launched"}), 200

def run_flask():
    app.run(port=PORT, debug=False)

def create_image():
    # Example for loading from a data URI (currently blank)
    data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGkAAABpCAYAAAA5gg06AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAExmlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSfvu78nIGlkPSdXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQnPz4KPHg6eG1wbWV0YSB4bWxuczp4PSdhZG9iZTpuczptZXRhLyc+CjxyZGY6UkRGIHhtbG5zOnJkZj0naHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyc+CgogPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9JycKICB4bWxuczpBdHRyaWI9J2h0dHA6Ly9ucy5hdHRyaWJ1dGlvbi5jb20vYWRzLzEuMC8nPgogIDxBdHRyaWI6QWRzPgogICA8cmRmOlNlcT4KICAgIDxyZGY6bGkgcmRmOnBhcnNlVHlwZT0nUmVzb3VyY2UnPgogICAgIDxBdHRyaWI6Q3JlYXRlZD4yMDI1LTA3LTIzPC9BdHRyaWI6Q3JlYXRlZD4KICAgICA8QXR0cmliOkV4dElkPjFkNjU5YzEyLTU4YWQtNDQzZi05YjhlLWI3NzYwNTEyYjUyYjwvQXR0cmliOkV4dElkPgogICAgIDxBdHRyaWI6RmJJZD41MjUyNjU5MTQxNzk1ODA8L0F0dHJpYjpGYklkPgogICAgIDxBdHRyaWI6VG91Y2hUeXBlPjI8L0F0dHJpYjpUb3VjaFR5cGU+CiAgICA8L3JkZjpsaT4KICAgPC9yZGY6U2VxPgogIDwvQXR0cmliOkFkcz4KIDwvcmRmOkRlc2NyaXB0aW9uPgoKIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PScnCiAgeG1sbnM6ZGM9J2h0dHA6Ly9wdXJsLm9yZy9kYy9lbGVtZW50cy8xLjEvJz4KICA8ZGM6dGl0bGU+CiAgIDxyZGY6QWx0PgogICAgPHJkZjpsaSB4bWw6bGFuZz0neC1kZWZhdWx0Jz5VbnRpdGxlZCBkZXNpZ24gLSAxPC9yZGY6bGk+CiAgIDwvcmRmOkFsdD4KICA8L2RjOnRpdGxlPgogPC9yZGY6RGVzY3JpcHRpb24+CgogPHJkZjpEZXNjcmlwdGlv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"
    if data_uri.startswith("data:image"):
        try:
            header, encoded = data_uri.split(",", 1)
            image_data = base64.b64decode(encoded)
            return Image.open(BytesIO(image_data))
        except Exception as e:
            print(f"Failed to load image from data URI: {e}")
    # fallback to generated image
    width = 64
    height = 64
    color1 = (0, 122, 204)
    color2 = (255, 255, 255)
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, 3 * width // 4, 3 * height // 4), fill=color2)
    return image

def on_clicked(icon, item=None):
    launch_ente_auth()

def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    icon = pystray.Icon("Ente Auth Tray", create_image(), "Ente Auth")
    icon.menu = pystray.Menu(
        pystray.MenuItem('Open Ente Auth', on_clicked, default=True),
        pystray.MenuItem('Quit', lambda icon, item: icon.stop())
    )

    icon.run()

if __name__ == "__main__":
    main()
