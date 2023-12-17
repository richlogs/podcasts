import tkinter as tk
from tkinter import ttk

import pandas as pd
from init.loging import get_logger

logger = get_logger()


def select_data(
    df: pd.DataFrame,
    columns: list[str] = ["title", "author", "duration", "download_date"],
) -> pd.DataFrame:
    return df[columns]


def select_folder():
    folder_path = tk.filedialog.askdirectory()
    logger.info(f"Selected Folder Path: {folder_path}")
    return folder_path


def get_selected_rows(tree):
    selected_items = tree.selection()
    for item in selected_items:
        item_data = tree.item(item, "values")
        print(item_data)  # or do something else with the data


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
