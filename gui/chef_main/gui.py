from pathlib import Path

from tkinter import messagebox, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\janerli\Desktop\колледж\kursach\gui\chef_main\assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def chefWindow(access_level):
    ChefWindow(access_level)


class ChefWindow(Toplevel):
    #
    # def open_admin_panel(self):
    #     if self.access_level == 'admin':
    #         pass # SettingsWindow(self)


    def __init__(self, access_level, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.access_level = access_level
        self.geometry("928x584")
        self.configure(bg="#CEAB83")

        self.canvas = Canvas(
            self,
            bg="#CEAB83",
            height=584,
            width=928,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            152.0,
            584.0,
            fill="#715E48",
            outline="")

        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            76.0,
            67.0,
            image=image_image_1
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))


        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        order_btn = Button(
            self.canvas,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        order_btn.place(
            x=0.0,
            y=332.0,
            width=152.0,
            height=43.0
        )

        button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        menu_btn = Button(
            self.canvas,
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        menu_btn.place(
            x=0.0,
            y=256.0,
            width=152.0,
            height=43.0
        )

        self.resizable(False, False)
        self.mainloop()