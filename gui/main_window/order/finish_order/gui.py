from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class FinishOrder(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg = "#CEAB83")
        self.parent = parent


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
            19.0,
            105.0,
            484.0,
            328.0,
            fill="#D9D9D9",
            outline="")

        self.canvas.create_rectangle(
            21.0,
            393.0,
            540.0,
            639.0,
            fill="#D9D9D9",
            outline="")

        self.canvas.create_text(
            19.0,
            8.0,
            anchor="nw",
            text="Выберите пиццу для настройки ингредиентов",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        self.canvas.create_text(
            22.0,
            333.0,
            anchor="nw",
            text="Ингредиенты:",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        self.canvas.create_text(
            12.0,
            655.0,
            anchor="nw",
            text="Итоговая стоимость: 0 руб.",
            fill="#000000",
            font=("Montserrat Alternates Regular", 24 * -1)
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
            x=641.0,
            y=473.0,
            width=57.04225540161133,
            height=54.0
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
            x=734.0,
            y=473.0,
            width=57.04225540161133,
            height=54.0
        )

        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        button_3 = Button(
            self.canvas,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        button_3.place(
            x=532.0,
            y=168.0,
            width=232.69927978515625,
            height=66.07679748535156
        )

        button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        button_4 = Button(
            self.canvas,
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        button_4.place(
            x=700.0,
            y=622.0,
            width=232.69927978515625,
            height=66.07679748535156
        )

