import sqlite3
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, ttk
from tkinter.ttk import Treeview

from database import conn
from gui.main_window.clients.add_client import AddClientWindow

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Clients(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg = "#CEAB83")


        self.canvas = Canvas(
            self,
            bg = "#CEAB83",
            height = 700,
            width = 948,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        style = ttk.Style()
        style.configure('mystyle2.Treeview', rowheight=50,font=('Montserrat Alternates', 9))
        style.configure('mystyle2.Treeview.Heading',
                        background='#715E48',
                        font=('Montserrat Alternates Bold', 11),
                        foreground='black')
        style.configure('mystyle2.Treeview.Cell', wraplength=230)

        self.tree = Treeview(self, columns=("client_id", "first_name", "last_name", "middle_name", "phone", "address"),
                             show="headings", style='mystyle2.Treeview')
        self.tree.heading("client_id", text="ID")
        self.tree.heading("first_name", text="Имя")
        self.tree.heading("last_name", text="Фамилия")
        self.tree.heading("middle_name", text="Отчество")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("address", text="Адрес")
        self.tree.column("client_id", width=20, anchor="center")
        self.tree.column("first_name", width=100, anchor="center")
        self.tree.column("last_name", width=100, anchor="center")
        self.tree.column("middle_name", width=100, anchor="center")
        self.tree.column("phone", width=120, anchor="center")
        self.tree.column("address", width=230, anchor="w")
        self.tree.place(x=42.0, y=95.0, width=865.0, height=571.0)
        self.load_clients()

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("img_2.png"))
        update_btn = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_clients,
            relief="flat"
        )
        update_btn.place(
            x=737.0,
            y=9.0,
            width=73.94,
            height=70.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("img_1.png"))
        add_btn = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_add_client_window,
            relief="flat"
        )
        add_btn.place(
            x=837.0,
            y=13.0,
            width=70,
            height=67
        )


        self.canvas.create_text(
            23.0,
            24.0,
            anchor="nw",
            text="Клиенты",
            fill="#000000",
            font=("Montserrat Alternates Bold", 36 * -1)
        )

    def load_clients(self):
        """Загружает данные клиентов из базы и отображает их в таблице."""
        for row in self.tree.get_children():
            self.tree.delete(row)


        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients")
        rows = cursor.fetchall()
        res = [tuple(row) for row in rows]

        for row in res:
            self.tree.insert("", "end", values=row)

    def open_add_client_window(self):
        """Открывает окно для добавления клиента."""
        AddClientWindow(self, conn, self.load_clients)

