from pathlib import Path

from tkinter import messagebox, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, StringVar, ttk
import tkinter.font as tkfont
import user_session
from database import conn
from gui.main_window.clients.gui import Clients
from gui.main_window.menu.gui import Menu
from gui.main_window.order.main import Order
from gui.main_window.order_history.gui import OrderHistory
from gui.main_window.statistic.gui import Statistic


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def show_custom_info(master, title, message):  # Added master parameter
    """Displays a custom info box with styling."""
    top = Toplevel(master)  # Привязка к родительскому окну
    top.title(title)


    top.transient(master=master) # модальное окно относительно родительского


    # Настройка шрифта
    montserrat_font = tkfont.Font(family="Montserrat Alternates", size=12, weight='bold')

    # Текстовое поле с сообщением
    msg_label = ttk.Label(top, text=message, font=montserrat_font, wraplength=300)
    msg_label.pack(pady=20)

    # Кнопка "OK"
    ok_button = ttk.Button(top, text="OK", command=top.destroy)
    ok_button.pack(pady=10)

    top.update_idletasks()

    top.resizable(False, False)
    top.geometry(
        f"+{int((top.winfo_screenwidth() - top.winfo_width()) / 2)}+{int((top.winfo_screenheight() - top.winfo_height()) / 2)}")
    top.iconphoto(False, PhotoImage(file="gui/icon.png"))
    # top.focus_force()
    top.grab_set()


class MainWindow(Toplevel):

    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)

        self.access_level = user_session.session.get_access_level()
        self.geometry("1100x700")
        self.configure(bg="#715E48")
        self.title("Chozabretta")
        self.iconphoto(False, PhotoImage(file="gui/icon.png"))
        self.center_window()


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

        self.windows = {
            "stat": Statistic(self),
            "ord": Order(self),
            "his": OrderHistory(self),
            "menu": Menu(self),
            "cli": Clients(self),
        }
        # messagebox.showinfo("Добро пожаловать", f"\nВаша роль: {self.access_level}\n")


        if self.access_level == 1:
            self.create_admin_buttons()
            self.show_welcome_message("Администратор")
            self.handle_btn_press("stat")

        elif self.access_level == 2:
            self.create_operator_buttons()
            self.show_welcome_message("Оператор")
            self.handle_btn_press("stat")

        elif self.access_level == 3:
            self.create_chef_buttons()
            self.show_welcome_message("Повар")
            self.handle_btn_press("ord")





        self.resizable(False, False)
        # self.protocol("WM_DELETE_WINDOW", func=self.quit_me())
        self.mainloop()

    def create_admin_buttons(self):
        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        admin_btn = Button(
            self.canvas,
            image=self.button_image_1,
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
        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        stats_btn = Button(
            self.canvas,
            image=self.button_image_2,
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

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        order_btn = Button(
            self.canvas,
            image=self.button_image_3,
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

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        menu_btn = Button(
            self.canvas,
            image=self.button_image_4,
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

        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        clients_btn = Button(
            self.canvas,
            image=self.button_image_5,
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

        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        history_btn = Button(
            self.canvas,
            image=self.button_image_6,
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

    def create_operator_buttons(self):
        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        stats_btn = Button(
            self.canvas,
            image=self.button_image_2,
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

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        order_btn = Button(
            self.canvas,
            image=self.button_image_3,
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

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        menu_btn = Button(
            self.canvas,
            image=self.button_image_4,
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

        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        clients_btn = Button(
            self.canvas,
            image=self.button_image_5,
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

        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        history_btn = Button(
            self.canvas,
            image=self.button_image_6,
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

    def create_chef_buttons(self):
        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        order_btn = Button(
            self.canvas,
            image=self.button_image_3,
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

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        menu_btn = Button(
            self.canvas,
            image=self.button_image_4,
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

    def show_welcome_message(self, name):
        show_custom_info(self, "Добро пожаловать", f"Ваша роль: {name}")

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

    def center_window(self):
        """Центрирует окно на экране."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        title_bar_height = 70
        y = (screen_height - window_height - title_bar_height) // 2
        x = (screen_width - window_width) // 2
        self.geometry(f"+{x}+{y}")

    def open_admin_panel(self):
        from gui.settings.admin_gui import AdminWindow
        if self.access_level == 1:  # Доступ только для администраторов (access_level = 2)
            AdminWindow(self, conn)
            #self.quit_me()# SettingsWindow(self)  # Ваше окно настроек
        else:
            messagebox.showerror("Ошибка доступа", "У вас нет прав доступа к админ-панели.")


