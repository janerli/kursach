from pathlib import Path

from tkinter import messagebox, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, StringVar

from gui.main_window.clients.gui import Clients
from gui.main_window.menu.gui import Menu
from gui.main_window.order.main import Order
from gui.main_window.order_history.gui import OrderHistory
from gui.main_window.statistic.gui import Statistic

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def mainWindow(access_level):
    MainWindow(access_level)



class MainWindow(Toplevel):

    def open_admin_panel(self):
        if self.access_level == 'admin':  # Доступ только для администраторов (access_level = 2)
            pass # SettingsWindow(self)  # Ваше окно настроек
        else:
            messagebox.showerror("Ошибка доступа", "У вас нет прав доступа к админ-панели.")

    def __init__(self, access_level, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.access_level = access_level
        self.geometry("1100x700")
        self.configure(bg="#715E48")
        self.title("Chozabretta")
        self.iconphoto(False, PhotoImage(file=relative_to_assets("image_1.png")))

        self.current_window = None
        self.current_window_label = StringVar()

        self.canvas = Canvas(
            self,
            bg="#715E48",
            height=700,
            width=1100,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            152.0,
            0.0,
            1100.0,
            700.0,
            fill="#CEAB83",
            outline=""
        )

        image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            76.0,
            67.0,
            image=image_image_1
        )

        button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        admin_btn = Button(
            self.canvas,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_admin_panel,
            relief="flat"
        )
        admin_btn.place(
            x=3.0,
            y=656.0,
            width=45.0,
            height=44.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        stats_btn = Button(
            self.canvas,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("stat"),
            relief="flat"
        )
        stats_btn.place(
            x=0.0,
            y=180.0,
            width=152.0,
            height=43.0
        )

        button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        order_btn = Button(
            self.canvas,
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("ord"),
            relief="flat"
        )
        order_btn.place(
            x=0.0,
            y=318.0,
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
            command=lambda: self.handle_btn_press("menu"),
            relief="flat"
        )
        menu_btn.place(
            x=0.0,
            y=249.0,
            width=152.0,
            height=43.0
        )

        button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        clients_btn = Button(
            self.canvas,
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("cli"),
            relief="flat"
        )
        clients_btn.place(
            x=0.0,
            y=387.0,
            width=152.0,
            height=43.0
        )

        button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        history_btn = Button(
            self.canvas,
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.handle_btn_press("his"),
            relief="flat"
        )
        history_btn.place(
            x=0.0,
            y=456.0,
            width=152.0,
            height=43.0
        )

        self.windows = {
            "stat": Statistic(self),
            "ord": Order(self),
            "his": OrderHistory(self),
            "menu": Menu(self),
            "cli": Clients(self),
        }

        self.handle_btn_press("stat")

        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.quit_me)
        self.mainloop()

    def handle_btn_press(self, frame_key):
        """Переключает отображение на указанный фрейм."""

        # Скрываем все окна
        for frame in self.windows.values():
            frame.place_forget()

        self.current_window = self.windows.get(frame_key)

        self.windows[frame_key].place(x=152, y=0, width=1100.0, height=700.0)

    def quit_me(self):
        self.quit()
        self.destroy()


