from tkinter import Toplevel, PhotoImage
from tkinter.ttk import Button, Label, Style, Entry
from database import (
    add_role,
    add_user,
    delete_user,
    update_user,
    update_client,
    delete_client,
)
from gui.main_window.main import MainWindow


class AdminWindow(Toplevel):
    def __init__(self, parent, conn, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.conn = conn
        self.configure(bg="#CEAB83")
        self.geometry("1100x700")
        self.title("Окно администратора")
        self.iconphoto(False, PhotoImage(file="gui/icon.png"))
        self.center_window()

        # Настройка стиля
        self.style = Style()
        self.style.configure(
            "TButton",
            font=("Montserrat Alternates", 12),
            background="#CEAB83",
            foreground="black",
            borderwidth=0,
        )
        self.style.map(
            "TButton",
            background=[("active", "#B8946B")],
            foreground=[("active", "white")],
        )

        # Создание элементов интерфейса
        self.create_widgets()

    def create_widgets(self):
        """Создаёт элементы интерфейса."""
        Label(
            self,
            text="Панель администратора",
            font=("Montserrat Alternates", 24),
            background="#CEAB83",
            foreground="black",
        ).place(x=350, y=50)

        # Кнопки
        buttons = [
            ("Добавить роль", self.open_add_role_window),
            ("Добавить пользователя", self.open_add_user_window),
            ("Удалить пользователя", self.open_delete_user_window),
            ("Редактировать пользователя", self.open_edit_user_window),
            ("Редактировать клиента", self.open_edit_client_window),
            ("Удалить клиента", self.open_delete_client_window),
            ("Назад", self.go_back),
        ]

        # Расположение кнопок
        for i, (text, command) in enumerate(buttons):
            Button(
                self,
                text=text,
                style="TButton",
                command=command,
            ).place(x=400, y=150 + i * 60, width=300, height=40)

    def open_add_role_window(self):
        self.open_form_window("Добавить роль", ["Название роли:"], lambda data: add_role(self.conn, data[0]))

    def open_add_user_window(self):
        self.open_form_window(
            "Добавить пользователя",
            ["Имя:", "Фамилия:", "Отчество:", "Логин:", "Пароль:", "ID уровня доступа:"],
            lambda data: add_user(self.conn, data[3], data[4], int(data[5]), data[0], data[1], data[2]),
        )

    def open_delete_user_window(self):
        self.open_form_window(
            "Удалить пользователя",
            ["ID пользователя:"],
            lambda data: delete_user(self.conn, int(data[0])),
        )

    def open_edit_user_window(self):
        self.open_form_window(
            "Редактировать пользователя",
            ["ID пользователя:", "Имя:", "Фамилия:", "Отчество:", "ID уровня доступа:"],
            lambda data: update_user(self.conn, int(data[0]), data[1], data[2], data[3], int(data[4])),
        )

    def open_edit_client_window(self):
        self.open_form_window(
            "Редактировать клиента",
            ["ID клиента:", "Имя:", "Фамилия:", "Отчество:", "Телефон:", "Адрес:"],
            lambda data: update_client(self.conn, int(data[0]), data[1], data[2], data[3], data[4], data[5]),
        )

    def open_delete_client_window(self):
        self.open_form_window(
            "Удалить клиента",
            ["ID клиента:"],
            lambda data: delete_client(self.conn, int(data[0])),
        )

    def open_form_window(self, title, fields, action):
        """Открывает окно с формой для заполнения данных."""
        modal = Toplevel(self)
        modal.geometry("400x500")
        modal.title(title)
        modal.configure(bg="#CEAB83")
        modal.iconphoto(False, PhotoImage(file="gui/icon.png"))

        Label(
            modal,
            text=title,
            font=("Montserrat Alternates", 16),
            background="#CEAB83",
            foreground="black",
        ).pack(pady=10)

        entries = []
        for i, field in enumerate(fields):
            Label(modal, text=field, font=("Montserrat Alternates", 14), background="#CEAB83").pack(pady=5)
            entry = Entry(modal)
            entry.pack(pady=5)
            entries.append(entry)

        def on_submit():
            data = [entry.get().strip() for entry in entries]
            try:
                action(data)
                modal.destroy()
                Label(self, text="Операция выполнена успешно!", font=("Arial", 12), background="#CEAB83").place(x=450, y=650)
            except Exception as e:
                Label(self, text=f"Ошибка: {e}", font=("Arial", 12), background="#CEAB83", foreground="red").place(x=450, y=650)

        Button(modal, text="Сохранить", style="TButton", command=on_submit).pack(pady=20)

    def go_back(self):
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
