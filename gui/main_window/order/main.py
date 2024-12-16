from pathlib import Path

from tkinter import Frame, Canvas, Entry, Text, Button, PhotoImage, messagebox

from gui.main_window.order.add_order.gui import AddOrder
from gui.main_window.order.finish_order.gui import FinishOrder
from gui.main_window.order.view_orders.gui import ViewOrder
from gui.main_window.order.choose_menu.gui import ChooseMenu

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

        self.configure(bg="#FFFFFF")

        self.user_id = None
        self.order_id = None
        self.delivery_type = None
        self.address = None
        self.total_price = None
        self.order_items = dict()

        self.windows = {
            "view": ViewOrder(self),
            "finish": FinishOrder(self, self.order_id, self.user_id, self.delivery_type, self.address, self.order_items, self.total_price),
            "add": AddOrder(self),
            "choose": ChooseMenu(self, self.user_id, self.delivery_type, self.address)
        }

        self.current_window = self.windows["view"]
        self.current_window.place(x=0, y=0, width=1100.0, height=700.0)

        self.current_window.tkraise()

    def navigate(self, name, *args):
        for window in self.windows.values():
            window.place_forget()

        if name == "choose":
            self.windows["choose"] = ChooseMenu(self, *args)
        elif name == "finish":
            self.windows["finish"] = FinishOrder(self, *args)
        # self.windows[name] = self.windows.get(name)

        self.windows[name].place(x=0, y=0, width=1100.0, height=700.0)
