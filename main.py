from customtkinter import *
import sqlite3

set_appearance_mode('System')
set_default_color_theme("blue")

class App(CTk):
    def __init__(self):
        super().__init__()

        w_width = 1280
        w_height = 760

        self.file = ""
        self.database_column_name = []
        self.info_database = []
        self.type_database = ['NULL', 'INTEGER', 'REAL', 'TEXT', 'BLOB']

        self.sql = sqlite3

        ### Configure Window
        self.title('DatabaseLite')
        self.geometry(f"{w_width}x{w_height}")

        ### Configure grid layout
        # self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        ### Create Widget in Left Sidebar
        self.sidebar_frame = CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = CTkLabel(self.sidebar_frame, text="Database Lite", font=CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_open = CTkButton(self.sidebar_frame, text="Otwórz bazę danych", command=self.open_database)
        self.sidebar_button_open.grid(row=1, column=0, padx=10, pady=10)
        self.sidebar_button_create = CTkButton(self.sidebar_frame, text="Stwórz bazę danych", command=self.create_database)
        self.sidebar_button_create.grid(row=2, column=0, padx=10, pady=10)
        self.sidebar_button_update = CTkButton(self.sidebar_frame, text="Edytuj bazę danych", command=self.update_database)
        self.sidebar_button_update.grid(row=3, column=0, padx=10, pady=10)
        self.apperance_mode_label = CTkLabel(self.sidebar_frame, text="Wygląd Motywu:", anchor="w")
        self.apperance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.apperance_mode_optionemenu = CTkOptionMenu(self.sidebar_frame, values=["System", "Dark", "Light"], command=self.change_apperance_mode_event)
        self.apperance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=10)
        self.scaling_label =CTkLabel(self.sidebar_frame, text="UI Scaling", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        ### Create tabview
        self.tabview = CTkTabview(self)
        self.tabview.grid(row=0, column=2, rowspan=4, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview.grid_columnconfigure((0), weight=1)
        self.tabview.add("Baza Danych")
        self.tabview.add("Nowa Baza Danych")
        self.tabview.add("Edycja Bazy Danych")
        self.tabview.tab("Baza Danych").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Nowa Baza Danych").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Edycja Bazy Danych").grid_columnconfigure(0, weight=1)

        ### Tabview [Baza Danych]
        self.optionmenu_1_frame = CTkFrame(self.tabview.tab("Baza Danych"))
        self.optionmenu_1_frame.pack(padx=10, pady=10)

        self.optionmenu_1_label = CTkLabel(self.optionmenu_1_frame, text='Wybierz zakładkę')
        self.optionmenu_1_label.grid(row=0, column=0, padx=20, pady=(10, 5))

        self.optionmenu_1 = CTkOptionMenu(self.optionmenu_1_frame, dynamic_resizing=False, values=[""])
        self.optionmenu_1.grid(row=1, column=0, padx=20, pady=(5, 20))

        ### Tabview [Nowa Baza Danych]
        self.optionmenu_3_frame = CTkFrame(self.tabview.tab("Nowa Baza Danych"))
        self.optionmenu_3_frame.pack(padx=10, pady=10)

        ### Tabview [Edycja Bazy Danych]
        self.optionmenu_3_frame = CTkFrame(self.tabview.tab("Edycja Bazy Danych"))
        self.optionmenu_3_frame.grid(row=0, column=0, padx=10, pady=10)

        self.optionmenu_3_label = CTkLabel(self.optionmenu_3_frame, text='Wybierz zakładkę')
        self.optionmenu_3_label.grid(row=0, column=0, padx=20, pady=(10, 5))

        self.optionmenu_3 = CTkOptionMenu(self.optionmenu_3_frame, dynamic_resizing=False, values=[""], command=self.change_column_in_the_database)
        self.optionmenu_3.grid(row=1, column=0, padx=20, pady=(5, 20))

        self.table_database_frame = CTkFrame(self.tabview.tab("Edycja Bazy Danych"))   

        ### Set default values
        self.apperance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    
    def open_database(self):
        ###
        self.file = filedialog.askopenfilename(filetypes=[('SQL Lite', '*.db'), ('Wszystkie Pliki', '*.*')])

        ###
        c = self.sql.connect(self.file)
        cursor = c.cursor()
        ###
        self.database_column_name = [a[0] for a in cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]

        ###
        self.optionmenu_1.configure(values=self.database_column_name)
        self.optionmenu_1.set(self.database_column_name[0])
        self.optionmenu_3.configure(values=self.database_column_name)
        self.optionmenu_3.set(self.database_column_name[0])

        ###
        self.change_column_in_the_database(self.database_column_name[0])

    def change_column_in_the_database(self, new_column_database: str):
        self.table_database_frame.destroy()
        try:
            ###
            cursor = self.sql.connect(self.file).cursor()

            ###
            self.info = [x for x in cursor.execute(f'PRAGMA table_xinfo({new_column_database})').fetchall()]

            ###
            self.table_database_frame = CTkFrame(self.tabview.tab("Edycja Bazy Danych"))
            self.table_database_frame.grid(row=1, column=0, padx=10, pady=10)
            

            ###
            rowid_label = CTkLabel(self.table_database_frame, text='rowID')
            rowid_label.grid(row=0, column=0, padx=(10, 5), pady=10)
            title_column_label = CTkLabel(self.table_database_frame, text='Nazwa kolumny')
            title_column_label.grid(row=0, column=1, padx=5, pady=10)     
            type_column_label = CTkLabel(self.table_database_frame, text='Typ kolumny')
            type_column_label.grid(row=0, column=2, padx=5, pady=10)
            notnull_label = CTkLabel(self.table_database_frame, text='notnull')
            notnull_label.grid(row=0, column=3, padx=5, pady=10)
            new_row_id_label = CTkLabel(self.table_database_frame, text='new rowid')
            new_row_id_label.grid(row=0, column=4, padx=5, pady=10)
            new_title_column_label = CTkLabel(self.table_database_frame, text='Nowa nazwa kolumn')
            new_title_column_label.grid(row=0, column=5, padx=5, pady=10)
            new_type_column_label = CTkLabel(self.table_database_frame, text='Nowy typ kolumny')
            new_type_column_label.grid(row=0, column=6, padx=5, pady=10)
            new_notnull_label = CTkLabel(self.table_database_frame, text='new notnull')
            new_notnull_label.grid(row=0, column=7, padx=(5,10), pady=10)

            ###
            for x in self.info:
                old_button_rowid = CTkButton(self.table_database_frame, text=x[0], width=50)
                old_button_rowid.grid(row=2+self.info.index(x), column=0, padx=5, pady=5)
                old_button_name = CTkButton(self.table_database_frame, text=x[1])
                old_button_name.grid(row=2+self.info.index(x), column=1, padx=5, pady=5)
                old_button_type = CTkButton(self.table_database_frame, text=x[2], width=100)
                old_button_type.grid(row=2+self.info.index(x), column=2, padx=5, pady=5)
                old_button_notnull = CTkButton(self.table_database_frame, text=x[3], width=50)
                old_button_notnull.grid(row=2+self.info.index(x), column=3, padx=5, pady=5)

                new_entry_rowid = CTkEntry(self.table_database_frame, placeholder_text=x[0])
                new_entry_rowid.grid(row=2+self.info.index(x), column=4, padx=5, pady=5)
                new_entry_name = CTkEntry(self.table_database_frame, placeholder_text=x[1])
                new_entry_name.grid(row=2+self.info.index(x), column=5, padx=5, pady=5)
                new_optionmenu_type = CTkOptionMenu(self.table_database_frame, values=self.type_database)
                new_optionmenu_type.set(value=f"{x[2]}")
                new_optionmenu_type.grid(row=2+self.info.index(x), column=6, padx=5, pady=5)
                new_optionmenu_notnull = CTkOptionMenu(self.table_database_frame, values=['0', '1'], width=60)
                new_optionmenu_notnull.set(value=f"{x[3]}")
                new_optionmenu_notnull.grid(row=2+self.info.index(x), column=7, padx=5, pady=5)
        except:
            print('Brak zakładki')

    def create_database(self):
        pass

    def update_database(self):
        pass

    def change_apperance_mode_event(self, new_appearance_mode: str):
        set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        set_widget_scaling(new_scaling_float)

    def open_input_dialog_event(self):
        dialog = CTkInputDialog(text="Type in a number:", title="Test")
        print("CTkInputDialog:", dialog.get_input())

if __name__ == "__main__":
    app = App()
    app.mainloop()




        # ### Create main entry and button
        # self.entry = CTkEntry(self, placeholder_text="entry")
        # self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=20, sticky="nsew")

        # self.main_button_1 = CTkButton(self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        # self.main_button_1.grid(row=3, column=3, padx=20, pady=20, sticky="nsew")

        # ### Create TextBox
        # self.textbox = CTkTextbox(self, width=250)
        # self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")


        # ### Create Radiobutton Frame
        # self.radiobutton_frame = CTkFrame(self)
        # self.radiobutton_frame.grid(row=0, column=3, padx=20, pady=(20, 0), sticky="nsew")
        # self.radio_var = IntVar(value=0)
        # self.label_radio_group = CTkLabel(self.radiobutton_frame, text="RadioButton Group:")
        # self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        # self.radio_button_1 = CTkRadioButton(self.radiobutton_frame, variable=self.radio_var, value=0)
        # self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_2 = CTkRadioButton(self.radiobutton_frame, variable=self.radio_var, value=1)
        # self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_3 = CTkRadioButton(self.radiobutton_frame, variable=self.radio_var, value=2)
        # self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # ### Create checkbox and switch frame
        # self.checkbox_slider_frame = CTkFrame(self)
        # self.checkbox_slider_frame.grid(row=1, column=3, padx=20, pady=(20, 0), sticky="nsew")
        # self.checkbox_1 = CTkCheckBox(self.checkbox_slider_frame)
        # self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")
        # self.checkbox_2 = CTkCheckBox(self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        # self.switch_1 = CTkSwitch(self.checkbox_slider_frame, command=lambda: print("switch 1 toggle"))
        # self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        # self.switch_2 = CTkSwitch(self.checkbox_slider_frame)
        # self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")

        # ### Create Slider and progressbar frame
        # self.slider_progressbar_frame = CTkFrame(self, fg_color="transparent")
        # self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        # self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)

        # self.seg_button_1 = CTkSegmentedButton(self.slider_progressbar_frame)
        # self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="ew")
        # self.progressbar_1 = CTkProgressBar(self.slider_progressbar_frame)
        # self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")
        # self.progressbar_2 = CTkProgressBar(self.slider_progressbar_frame)
        # self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=10, sticky="ew")
        # self.slider_1 = CTkSlider(self.slider_progressbar_frame, from_=0, to=0, number_of_steps=4)
        # self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=10, sticky="ew")
        # self.slider_2 = CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        # self.slider_2.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
        # self.progressbar_3 = CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        # self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=10, sticky="ns")


        ### Set default values ------------------------
        # self.sidebar_button_update.configure(state="disabled", text="Disabled Button")
        # self.checkbox_2.configure(state="disabled")
        # self.switch_2.configure(state="disabled")
        # self.checkbox_1.select()
        # self.switch_1.select()
        # self.radio_button_3.configure(state="disabled")

        # self.optionmenu_1.set("CTkOptiomenu")
        # self.combobox_1.set("CTkCOmboBox")
        # self.slider_1.configure(command=self.progressbar_2.set)
        # self.slider_2.configure(command=self.progressbar_3.set)
        # self.progressbar_1.start()
        # self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        # self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        # self.seg_button_1.set("Value 2")