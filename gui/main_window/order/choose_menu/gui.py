from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ChooseMenu(Frame):
    def __init__(self, parent, user_id, delivery_type, address, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg = "#CEAB83")
        self.parent = parent
        self.user_id = user_id
        self.delivery_type = delivery_type
        self.address = address


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
            22.0,
            78.0,
            891.0,
            275.0,
            fill="#D9D9D9",
            outline="")

        self.canvas.create_rectangle(
            22.0,
            408.0,
            891.0,
            618.0,
            fill="#D9D9D9",
            outline="")

        self.canvas.create_text(
            22.0,
            18.0,
            anchor="nw",
            text="Меню:",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        self.canvas.create_text(
            32.0,
            346.0,
            anchor="nw",
            text="Текущий заказ:",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
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
            x=660.0,
            y=280.0,
            width=73.94366455078125,
            height=70.0
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
            x=780.5556640625,
            y=280.0,
            width=73.94366455078125,
            height=70.0
        )

        self.canvas.create_text(
            21.0,
            653.0,
            anchor="nw",
            text="Итоговая стоимость: 0 руб.",
            fill="#000000",
            font=("Montserrat Alternates Regular", 24 * -1)
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
            x=749.0,
            y=631.0,
            width=193.17681884765625,
            height=54.85408401489258
        )

