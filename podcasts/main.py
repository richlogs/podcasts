import tkinter as tk
from tkinter import ttk

import customtkinter
from init.loging import get_logger
from utils.gui import get_selected_rows, select_data, select_folder, set_tk_style
from utils.sqlite import get_podcast_data

logger = get_logger()

df = get_podcast_data()
df = select_data(df)


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
root = customtkinter.CTk()
root.geometry("500x500")
frame = customtkinter.CTkFrame(root)
frame.pack(pady=10, padx=20, fill="both", expand=True)


set_tk_style()
tree = ttk.Treeview(frame, columns=list(df.columns), show="headings")

# Defining column headings
for column in tree["columns"]:
    tree.heading(column, text=column)

# Inserting the DataFrame rows
for _, row in df.iterrows():
    tree.insert("", "end", values=list(row))

tree.pack(expand=True, fill="both")

# Button to get selected rows
select_button = tk.Button(frame, text="Get Selected Rows", command=get_selected_rows)
select_button.pack()


folder_button = tk.Button(frame, text="Select Folder", command=select_folder)
folder_button.pack()

# Label to display selected folder path
folder_label = tk.Label(frame, text="", wraplength=300)
folder_label.pack()


# Running the application
root.mainloop()
