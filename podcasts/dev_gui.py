import customtkinter

import podcasts.utils.dbops as dbops
import podcasts.utils.data_processing as data_processing

df_podcasts = dbops.get_podcast_data()
df_podcasts = data_processing.convert_duration(df_podcasts)
df_podcasts = data_processing.add_status(df_podcasts)
df_podcasts = data_processing.select_data(df_podcasts)

x = 3


class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.values = values
        self.title = title
        self.checkboxes = []

        self.title = customtkinter.CTkLabel(
            self, text=self.title, fg_color="gray30", corner_radius=6
        )
        self.title.grid(row=0, column=0, padx=(4, 4), pady=(10, 0), sticky="ew")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i + 1, column=0, padx=5, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes


class MyTableFrame(customtkinter.CTkFrame):
    def __init__(self, master, title):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.title = title

        self.title = customtkinter.CTkLabel(
            self, text=self.title, font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.title.grid(row=0, column=0, padx=(10, 10), pady=(20, 0), sticky="ew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Merry Christmas Dad!")
        self.geometry("400x220")

        # configure grid layout
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0), weight=1)

        # create sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=2)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # add sidebar label
        self.sidebar_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Filtering Options",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.sidebar_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # add playstatus checkboxes and button
        self.playstatus_checkbox = MyCheckboxFrame(
            self.sidebar_frame,
            title="Play Status",
            values=["Played", "Listening", "Unplayed"],
        )
        self.playstatus_checkbox.grid(
            row=1, column=0, padx=(10, 10), pady=(10, 0), sticky="nsew"
        )
        self.playstatus_checkbox.configure(fg_color="transparent")

        self.playstatus_button = customtkinter.CTkButton(
            self.sidebar_frame, text="Apply", command=self.playstatus_filters
        )
        self.playstatus_button.grid(
            row=2, column=0, padx=(10, 10), pady=(10, 0), sticky="ew"
        )

        # create table frame
        self.table_frame = MyTableFrame(self, title="Podcasts")
        self.table_frame.grid(row=0, column=1, sticky="nsew")

    def playstatus_filters(self):
        print(f"Play status filters: {self.playstatus_checkbox.get()}")


app = App()
app.mainloop()
