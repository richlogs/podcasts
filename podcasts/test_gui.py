import customtkinter

import podcasts.utils.data_processing as data_processing
import podcasts.utils.dbops as dbops
import podcasts.utils.gui as gui


class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = self.create_checkboxes()

    def create_checkboxes(self):
        checkboxes = []
        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i + 1, column=0, padx=5, pady=(10, 0), sticky="w")
            checkboxes.append(checkbox)
        return checkboxes

class MyTableFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title
        self.title_label = customtkinter.CTkLabel(self, text=self.title, fg_color="gray30", corner_radius=6)
        self.title_label.grid(row=0, column=0, padx=(4, 4), pady=(10, 0), sticky="ew")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Podcast Manager")
        self.geometry("1200x800")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = customtkinter.CTkFrame(self)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        self.gui_elements = {
            'search_box': customtkinter.CTkSearchBox(self.sidebar_frame),
            'playstatus_checkbox': MyCheckboxFrame(self.sidebar_frame, title="Play Status", values=["Played", "Listening", "Unplayed"]),
            'playstatus_button': customtkinter.CTkButton(self.sidebar_frame, text="Apply", command=self.playstatus_filters),
            'directory_button': customtkinter.CTkButton(self.sidebar_frame, text="Select Folder", command= lambda: gui.select_folder(self.directory_button.cget("textvariable"))),
            'move_files_button': customtkinter.CTkButton(self.sidebar_frame, text="Move Files", command= lambda: gui.move_files(self.table, self.directory_button.cget("textvariable"))),
            'table_frame': MyTableFrame(self, title="Podcasts"),
            'table': gui.build_table(self.table_frame, df=df_podcasts)
        }

        self.gui_elements['search_box'].search_string.trace_add("write", self.search_bar_filters)

    def filter_table(self, filter_func):
        table_items = self.gui_elements['table'].get_children()

        for item in table_items:
            if filter_func(self.gui_elements['table'].item(item)['values']):
                search_var = self.gui_elements['table'].item(item)['values']
                self.gui_elements['table'].delete(item)
                self.gui_elements['table'].insert("", 0, values=search_var)

    def playstatus_filters(self):
        filters = self.gui_elements['playstatus_checkbox'].get()
        self.filter_table(lambda values: values[2] in filters)

    def search_bar_filters(self, *args):
        filters = self.gui_elements['search_box'].search_string.get()
        self.filter_table(lambda values: filters.lower() in values[1].lower())

def process_podcast_data(df):
    df = data_processing.convert_duration(df)
    df = data_processing.add_status(df)
    df = data_processing.select_data(df)
    df = data_processing.format_columns(df)
    return df

df_podcasts = process_podcast_data(dbops.get_podcast_data())

app = App()
app.mainloop()
