import json
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from rpatool import RenPyArchive

CONFIG_PATH = os.path.join(sys._MEIPASS, "config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        messagebox.showerror("Error", f"Configuration file '{CONFIG_PATH}' not found!")
        sys.exit(1)
    
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

config = load_config()

game_exe_name = config["game_exe_name"]
archive_relative_path = config["archive_relative_path"]
mod_folder_path = config["mod_folder_path"]
icon_file = config["icon_file"]
app_title = config["app_title"]

isExeFound = False

def get_target_folder(target_folder):
    global isExeFound
    while True:
        folder = filedialog.askdirectory(title="Choose game folder")
        if not folder:
            break

        game_exe = os.path.join(folder, game_exe_name)
        if not os.path.exists(game_exe):
            messagebox.showerror("Error", "Cannot find the game exe file!")
            isExeFound = False
        else:
            target_folder.set(folder)
            isExeFound = True
            break

def update_archive(archive_path, mod_folder_path, progress_bar):
    try:
        archive = RenPyArchive(archive_path)

        file_list = archive.list()

        normalized_file_list = [file.replace("\\", "/") for file in file_list]

        mod_files = []
        for root, dirs, files in os.walk(mod_folder_path):
            for file_name in files:
                mod_file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(mod_file_path, mod_folder_path)
                normalized_relative_path = relative_path.replace("\\", "/")
                mod_files.append((mod_file_path, normalized_relative_path))

        total_files = len(mod_files)
        progress_step = 70 / total_files
        current_progress = 0

        for mod_file_path, normalized_relative_path in mod_files:
            if normalized_relative_path in normalized_file_list:
                print(f"File was found in archive: {normalized_relative_path}. Rewriting...")
                archive.remove(normalized_relative_path)
            else:
                print(f"File was not found in archive: {normalized_relative_path}. Adding...")

            archive.add(normalized_relative_path, open(mod_file_path, "rb").read())

            current_progress += progress_step
            progress_bar['value'] = current_progress
            progress_bar.update_idletasks()

        print("Saving changes.")
        archive.save(archive_path)
        print("Archive update completed.")

        progress_bar['value'] = 100
        progress_bar.update_idletasks()

        messagebox.showinfo("Success", "Installation completed!")

    except Exception as e:
        return messagebox.showerror("Error", f"Error when installing a mod to an archive: {e}")

def installation(target_folder, progress_bar, root):
    mod_folder = 'mod/'
    if hasattr(sys, '_MEIPASS'):
        mod_folder = os.path.join(sys._MEIPASS, 'mod/')
    
    if not os.path.exists(mod_folder):
        messagebox.showerror("Error", "Folder 'mod' was not found!")
        return
    
    if not os.path.exists(os.path.join(target_folder.get(), archive_relative_path)):
        messagebox.showerror("Error", "RPA archive was not found!")
        return

    if not isExeFound:
        messagebox.showerror("Error", "Game folder was not selected!")
        return
    else:
        update_archive(os.path.join(target_folder.get(), archive_relative_path), mod_folder, progress_bar)
        
        return root.destroy()

def start():
    root = Tk()
    root.title(app_title)
    root.resizable(False, False)
    if hasattr(sys, '_MEIPASS'):
        icon_path = os.path.join(sys._MEIPASS, icon_file)
    else:
        icon_path = icon_file
    
    root.iconbitmap(icon_path)
    
    mainframe = ttk.Frame(root, padding="12 12 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    ttk.Label(mainframe, text="Game folder path:").grid(column=1, row=1, sticky=W)
    target_folder = StringVar()
    
    progress_bar = ttk.Progressbar(mainframe, orient=HORIZONTAL, length=100, mode='determinate')
    progress_bar.grid(column=1, row=4, columnspan=2, pady=2, sticky=(W, E))
    
    ttk.Entry(mainframe, width=50, state=DISABLED, textvariable=target_folder).grid(column=1, row=2, sticky=W)
    ttk.Button(mainframe, text="Browse", command=lambda: get_target_folder(target_folder)).grid(column=2, row=2, padx=1, sticky=W)
    ttk.Button(mainframe, text="Install", command=lambda: installation(target_folder, progress_bar, root)).grid(column=1, row=3, columnspan=2, pady=3, sticky=(W, E))
    ttk.Separator(mainframe, orient=HORIZONTAL).grid(column=1, row=5, columnspan=2, pady=(10, 0), sticky=(W, E))
    style = ttk.Style()
    style.configure("GrayText.TLabel", foreground="gray")
    translator = ttk.Label(mainframe, style="GrayText.TLabel", text="Mod Author: <insert name here>")
    translator.grid(column=1, row=6, sticky=W)
    installer = ttk.Label(mainframe, style="GrayText.TLabel", text="Installer Author: djighoul29")
    installer.grid(column=2, row=6, sticky=E)
    telegram = ttk.Label(mainframe, style="GrayText.TLabel", text="<some text or link here>")
    telegram.grid(column=1, row=7, sticky=W)

    root.mainloop()

if __name__ == "__main__":
    start()