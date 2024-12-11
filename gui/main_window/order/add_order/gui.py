from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class AddOrder(Frame):
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
        self.canvas.create_text(
            21.0,
            21.0,
            anchor="nw",
            text="Добавление заказа",
            fill="#000000",
            font=("Montserrat Alternates Bold", 36 * -1)
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=581.0,
            y=498.0,
            width=232.69927978515625,
            height=66.07679748535156
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self.canvas,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=509.0,
            y=7.0,
            width=158.0,
            height=71.0
        )

        self.canvas.create_text(
            69.0,
            160.0,
            anchor="nw",
            text="ID Клиента",
            fill="#000000",
            font=("Montserrat Alternates Regular", 32 * -1)
        )

        self.canvas.create_text(
            69.0,
            258.0,
            anchor="nw",
            text="Тип доставки",
            fill="#000000",
            font=("Montserrat Alternates Regular", 32 * -1)
        )

        self.canvas.create_text(
            69.0,
            352.0,
            anchor="nw",
            text="Адрес",
            fill="#000000",
            font=("Montserrat Alternates Regular", 32 * -1)
        )

        self.canvas.create_rectangle(
            380.0,
            247.0,
            587.0,
            309.0,
            fill="#D9D9D9",
            outline="")

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            442.0,
            375.0,
            image=entry_image_1
        )
        entry_1 = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=220.0,
            y=344.0,
            width=444.0,
            height=60.0
        )

        entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            441.5,
            180.0,
            image=entry_image_2
        )
        entry_2 = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0
        )
        entry_2.place(
            x=320.0,
            y=149.0,
            width=243.0,
            height=60.0
        )

        self.canvas.create_rectangle(
            664.0,
            247.0,
            871.0,
            309.0,
            fill="#D9D9D9",
            outline="")

