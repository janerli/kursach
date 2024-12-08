from pathlib import Path
from database import conn
from tkinter import messagebox, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel
from ..admin_main.main import adminWindow
from ..chef_main.gui import chefWindow
from ..operator_main.gui import opWindow
import database

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\janerli\Desktop\колледж\kursach\gui\login\assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def loginWindow():
    Login()


class Login(Toplevel):
    # global access
    def on_login(self):
        username = self.username.get()
        password = self.password.get()
        user_id, access_level = database.check_login(conn, username, password)
        if user_id:
            self.destroy()
            if access_level=='admin':
                adminWindow(access_level)
            elif access_level=='operator':
                opWindow(access_level)
                pass
            elif access_level=='chef':
                chefWindow(access_level)
                pass
            return
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.geometry("928x584")
        self.configure(bg="#FFFFFF")

        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=584,
            width=928,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            464.0,
            292.0,
            image=image_image_1
        )

        self.canvas.create_text(
            556.0,
            122.0,
            anchor="nw",
            text="Авторизация",
            fill="#FFFFFF",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(
            695.0,
            250.0,
            image=image_image_2
        )

        image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(
            690.0,
            364.0,
            image=image_image_3
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_login,
            relief="flat"
        )
        button_1.place(
            x=604.0,
            y=435.0,
            width=185.0,
            height=58.0
        )

        self.canvas.create_text(
            563.0,
            189.0,
            anchor="nw",
            text="Логин",
            fill="#FFFFFF",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.canvas.create_text(
            563.0,
            302.0,
            anchor="nw",
            text="Пароль",
            fill="#FFFFFF",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        image_image_4 = PhotoImage(
            file=relative_to_assets("image_4.png"))
        image_4 = self.canvas.create_image(
            216.0,
            324.0,
            image=image_image_4
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            696.0,
            365.0,
            image=entry_image_1
        )
        self.password = Entry(
            self.canvas,
            bd=0,
            bg="#F5F5F5",
            fg="#000716",
            highlightthickness=0,
            show='*'
        )
        self.password.place(
            x=560.0,
            y=347.0,
            width=272.0,
            height=34.0
        )

        entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            699.0,
            250.0,
            image=entry_image_2
        )
        self.username = Entry(
            self.canvas,
            bd=0,
            bg="#F5F5F5",
            fg="#000716",
            highlightthickness=0
        )
        self.username.place(
            x=563.0,
            y=232.0,
            width=272.0,
            height=34.0
        )

        image_image_5 = PhotoImage(
            file=relative_to_assets("image_5.png"))
        image_5 = self.canvas.create_image(
            216.0,
            141.0,
            image=image_image_5
        )


        self.resizable(False, False)
        self.mainloop()
