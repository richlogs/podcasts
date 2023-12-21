import os
import shutil
import tkinter as tk
from tkinter import ttk

from podcasts.init.loging import get_logger

logger = get_logger()


def move_files(dest_dir, file_paths):
    for file_path in file_paths:
        # Get the base name of the file to preserve the original file name
        base_name = os.path.basename(file_path)
        # Define the destination file path
        dest_file_path = os.path.join(dest_dir, base_name)
        # Move the file
        shutil.move(file_path, dest_file_path)


def select_folder():
    folder_path = tk.filedialog.askdirectory()
    logger.info(f"Selected Folder Path: {folder_path}")
    return folder_path


def get_selected_rows(tree):
    selected_items = tree.selection()
    final_column_values = []
    for item in selected_items:
        item_data = tree.item(item, "values")
        if item_data:  # check if item_data is not empty
            final_column_value = item_data[-1]  # get the last value
            final_column_values.append(final_column_value)
    logger.info(f"Selected information: {final_column_values}")
    return final_column_values


def set_tk_style():
    style = ttk.Style()

    style.theme_use("default")

    style.configure(
        "Treeview",
        background="#2a2d2e",
        foreground="white",
        rowheight=25,
        fieldbackground="#343638",
        bordercolor="#343638",
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", "#22559b")])

    style.configure(
        "Treeview.Heading", background="#565b5e", foreground="white", relief="flat"
    )
    style.map("Treeview.Heading", background=[("active", "#3484F0")])


if __name__ == "__main__":
    from podcasts.utils.sqlite import get_podcast_data

    df = get_podcast_data()
    print(df)
    x = 3
