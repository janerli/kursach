from pathlib import Path

from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox

from gui.main_window.order.add_order.gui import AddOrder
from gui.main_window.order.choose_menu.gui import ChooseMenu
from gui.main_window.order.finish_order.gui import FinishOrder
from gui.main_window.order.view_orders.gui import ViewOrder

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# def guests():
#     Guests()


class Order(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_rid = None

        self.configure(bg="#FFFFFF")

        # Loop through windows and place them
        self.windows = {
            "view": ViewOrder(self),
            "finish": FinishOrder(self),
            "add": AddOrder(self),
            "choose": ChooseMenu(self)
        }

        self.current_window = self.windows["view"]
        self.current_window.place(x=0, y=0, width=1100.0, height=700.0)

        self.current_window.tkraise()

    def navigate(self, name):
        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Show the screen of the button pressed
        self.windows[name].place(x=0, y=0, width=1100.0, height=700.0)