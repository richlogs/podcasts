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
root.geometry("500x500")
frame = customtkinter.CTkFrame(root)
frame.pack(pady=10, padx=20, fill="both", expand=True)


gui.set_tk_style()
tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")

# Defining column headings
for column in tree["columns"]:
    tree.heading(column, text=column)

# Inserting the DataFrame rows
for _, row in df.iterrows():
    tree.insert("", "end", values=list(row))

tree.pack(expand=True, fill="both")

# Button to move selected rows to folder
select_button = tk.Button(
    frame, text="Move Selected to Folder", command=lambda: gui.move_files(tree, folder_label.cget("text"))
)
select_button.pack()


folder_button = tk.Button(frame, text="Select Folder", command=lambda: folder_label.config(text=gui.select_folder()))
folder_button.pack()

# Label to display selected folder path
folder_label = tk.Label(frame, text="", wraplength=300)
folder_label.pack()


# Running the application
root.mainloop()
