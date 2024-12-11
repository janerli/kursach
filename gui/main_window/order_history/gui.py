
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class OrderHistory(Frame):
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
        self.canvas.create_rectangle(
            21.0,
            161.0,
            927.0,
            631.0,
            fill="#D9D9D9",
            outline="")

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=830.0,
            y=633.7333984375,
            width=70.0,
            height=66.26666259765625
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            234.5,
            49.0,
            image=self.entry_image_1
        )
        entry_1 = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=170.0,
            y=26.0,
            width=129.0,
            height=44.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            671.5,
            117.0,
            image=self.entry_image_2
        )
        entry_2 = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_2.place(
            x=607.0,
            y=94.0,
            width=129.0,
            height=44.0
        )

        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(
            671.5,
            49.0,
            image=self.entry_image_3
        )
        entry_3 = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_3.place(
            x=607.0,
            y=26.0,
            width=129.0,
            height=44.0
        )

        self.entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = self.canvas.create_image(
            234.5,
            117.0,
            image=self.entry_image_4
        )
        entry_4 = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_4.place(
            x=170.0,
            y=94.0,
            width=129.0,
            height=44.0
        )

        self.canvas.create_text(
            21.0,
            37.0,
            anchor="nw",
            text="ID заказа",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.canvas.create_text(
            402.0,
            37.0,
            anchor="nw",
            text="Дата заказа",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.canvas.create_text(
            402.0,
            105.0,
            anchor="nw",
            text="Итоговая сумма",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.canvas.create_text(
            21.0,
            105.0,
            anchor="nw",
            text="ID клиента",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=786.0,
            y=20.0,
            width=158.0,
            height=120.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        button_3 = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        button_3.place(
            x=672.0,
            y=633.7333984375,
            width=70.0,
            height=66.26666259765625
        )

