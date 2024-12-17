from pathlib import Path

from tkinter import Toplevel, Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox

import user_session
from ..main_window.main import mainWindow
from database import conn
import database


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class Login(Toplevel):

    def on_login(self):
        username = self.username.get()
        password = self.password.get()
        user_id, access_level = database.check_login(conn, username, password)
        if user_id:
            self.destroy()
            user_session.session.set_access_level(access_level)
            mainWindow(access_level)
            return
        else:
            messagebox.showerror("Ошибка", "Неправильный логин или пароль")

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.geometry("1100x700")
        self.configure(bg = "#FFFFFF")


        self.canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 700,
            width = 1100,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            635.0,
            399.0,
            image=image_image_1
        )

        self.canvas.create_text(
            647.0,
            89.0,
            anchor="nw",
            text="Авторизация",
            fill="#FFFFFF",
            font=("Montserrat Alternates Regular", 40 * -1)
        )

        image_image_2 = PhotoImage(
            file=relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(
            790.0,
            268.0,
            image=image_image_2
        )

        image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(
            790.0,
            438.0,
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
            x=803.0,
            y=579.0,
            width=272.0,
            height=85.27567291259766
        )

        self.canvas.create_text(
            567.0,
            174.0,
            anchor="nw",
            text="Логин",
            fill="#FFFFFF",
            font=("Montserrat Alternates Regular", 32 * -1)
        )

        self.canvas.create_text(
            567.0,
            344.0,
            anchor="nw",
            text="Пароль",
            fill="#FFFFFF",
            font=("Montserrat Alternates Regular", 32 * -1)
        )

        image_image_4 = PhotoImage(
            file=relative_to_assets("image_4.png"))
        image_4 = self.canvas.create_image(
            229.0,
            344.0,
            image=image_image_4
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            799.5,
            439.0,
            image=entry_image_1
        )
        self.password = Entry(
            self.canvas,
            bd=0,
            bg="#F5F5F5",
            fg="#000716",
            highlightthickness=0,
            show='*',
            font=("Montserrat Alternates Regular", 32 * -1)
        )
        self.password.place(
            x=589.0,
            y=411.0,
            width=421.0,
            height=54.0
        )

        entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            795.5,
            267.0,
            image=entry_image_2
        )
        self.username = Entry(
            self.canvas,
            bd=0,
            bg="#F5F5F5",
            fg="#000716",
            highlightthickness=0,
            font=("Montserrat Alternates Regular", 32 * -1)
        )
        self.username.place(
            x=585.0,
            y=239.0,
            width=421.0,
            height=54.0
        )

        image_image_5 = PhotoImage(
            file=relative_to_assets("image_5.png"))
        image_5 = self.canvas.create_image(
            229.0,
            162.0,
            image=image_image_5
        )


        self.resizable(False, False)
        self.mainloop()
