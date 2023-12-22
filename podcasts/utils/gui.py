import os
import shutil
import tkinter as tk
from tkinter import ttk
from urllib.parse import unquote

import pandas as pd

import podcasts.utils.gui as gui
from podcasts.init.loging import get_logger

logger = get_logger()

def select_folder(button):
    folder_path = tk.filedialog.askdirectory(initialdir=os.path.expanduser("~"))
    button.configure(textvariable=folder_path)
    logger.info(f"Selected Folder Path: {folder_path}")


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

def copy_files(file_urls, target_directory):
    if not os.path.exists(target_directory):
        print(f"aint no dir named {target_directory}")

    for file_url in file_urls:
        file_path = unquote(file_url.replace('file://', ''))
        file_name = os.path.basename(file_path)
        destination = os.path.join(target_directory, file_name)
        shutil.copy(file_path, destination)
        print(f"Moved '{file_name}' to '{target_directory}'")

def move_files(tree, dest_dir):
    print(dest_dir)
    files = get_selected_rows(tree)
    copy_files(files, dest_dir)

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


def build_table(master: str, df: pd.DataFrame):
    gui.set_tk_style()
    tree = ttk.Treeview(master, columns=list(df.columns), show="headings")
    for column in tree["columns"]:
        tree.heading(column, text=column)

    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    return tree




if __name__ == "__main__":
    pass

    # df = get_podcast_data()
    # print(df)
    # x = 3

    files = ['file:///Users/richardkyle/Library/Group%20Containers/243LU875E5.groups.com.apple.podcasts/Library/Cache/88AEC123-4EF8-4DF4-A39B-E931F3E00F68.mp3',
     'file:///Users/richardkyle/Library/Group%20Containers/243LU875E5.groups.com.apple.podcasts/Library/Cache/D6A10E8E-0E7F-492D-B60D-D8375E69AD30.mp3',
     'file:///Users/richardkyle/Library/Group%20Containers/243LU875E5.groups.com.apple.podcasts/Library/Cache/74A89B4C-9004-4446-874F-930C411D31E5.mp3']


    def copy_files(file_urls, target_directory):
    # Ensure the target directory exists, create it if it does not
        if not os.path.exists(target_directory):
            print(f"aint no dir named {target_directory}")

        # Iterate through the list of file URLs
        for file_url in file_urls:
            # Parse the file URL to get the local file path
            file_path = unquote(file_url.replace('file://', ''))

            # Extract the file name from the path
            file_name = os.path.basename(file_path)

            # Define the destination path for the file
            destination = os.path.join(target_directory, file_name)

            # Move the file to the target directory
            shutil.copy(file_path, destination)
            print(f"Moved '{file_name}' to '{target_directory}'")

    move_files(files, '/Users/richardkyle/Desktop/test')
