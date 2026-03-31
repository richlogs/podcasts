import tkinter as tk
from tkinter import ttk

import customtkinter
import utils.gui as gui
from init.loging import get_logger

import podcasts.utils.data_processing as data_processing
from podcasts.utils.dbops import get_podcast_data

logger = get_logger()

df = get_podcast_data()
df = data_processing.convert_duration(df)
df = data_processing.add_status(df)
df = data_processing.select_data(df)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.title("Podcasts")
root.geometry("700x550")

frame = customtkinter.CTkFrame(root)
frame.pack(pady=10, padx=20, fill="both", expand=True)

# --- Step 1: Folder selection ---
folder_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
folder_frame.pack(fill="x", padx=10, pady=(10, 4))

customtkinter.CTkLabel(folder_frame, text="Destination folder:", anchor="w").pack(side="left")

folder_path_label = customtkinter.CTkLabel(
    folder_frame, text="None selected", text_color="gray", anchor="w"
)
folder_path_label.pack(side="left", padx=8, fill="x", expand=True)

def on_select_folder():
    path = gui.select_folder()
    if path:
        folder_path_label.configure(text=path, text_color="white")
        _refresh_move_button()

customtkinter.CTkButton(
    folder_frame, text="Browse", width=80, command=on_select_folder
).pack(side="right")

# --- Episode table ---
gui.set_tk_style()
tree = ttk.Treeview(frame, columns=list(df.columns), show="headings", selectmode="extended")

for column in tree["columns"]:
    tree.heading(column, text=column)

for _, row in df.iterrows():
    tree.insert("", "end", values=list(row))

tree.pack(expand=True, fill="both", padx=10, pady=(4, 0))

# --- Selection count ---
selection_label = customtkinter.CTkLabel(frame, text="0 episodes selected", text_color="gray", anchor="w")
selection_label.pack(fill="x", padx=12, pady=(2, 0))

def on_selection_change(event=None):
    n = len(tree.selection())
    selection_label.configure(text=f"{n} episode{'s' if n != 1 else ''} selected")
    _refresh_move_button()

tree.bind("<<TreeviewSelect>>", on_selection_change)

# --- Move button + status ---
bottom_frame = customtkinter.CTkFrame(frame, fg_color="transparent")
bottom_frame.pack(fill="x", padx=10, pady=(6, 10))

status_label = customtkinter.CTkLabel(bottom_frame, text="", anchor="w")
status_label.pack(side="left", fill="x", expand=True)

def on_move():
    dest = folder_path_label.cget("text")
    if dest == "None selected":
        status_label.configure(text="Please select a destination folder first.", text_color="#e06c75")
        return
    if not tree.selection():
        status_label.configure(text="Please select at least one episode.", text_color="#e06c75")
        return
    try:
        gui.move_files(tree, dest)
        n = len(tree.selection())
        status_label.configure(
            text=f"{n} episode{'s' if n != 1 else ''} moved successfully.", text_color="#98c379"
        )
    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="#e06c75")
        logger.error(e)

move_button = customtkinter.CTkButton(
    bottom_frame, text="Move Selected Episodes", command=on_move, state="disabled"
)
move_button.pack(side="right")

def _refresh_move_button():
    folder_chosen = folder_path_label.cget("text") != "None selected"
    rows_selected = len(tree.selection()) > 0
    move_button.configure(state="normal" if folder_chosen and rows_selected else "disabled")

root.mainloop()
