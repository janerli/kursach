import sqlite3
from tkinter import Toplevel, messagebox
from tkinter.ttk import Label, Entry, Button


class AddClientWindow(Toplevel):
    """
    Окно для добавления клиента.
    """
    def __init__(self, parent, conn, refresh_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.conn = conn
        self.refresh_callback = refresh_callback
        self.title("Добавить клиента")
        self.center_window()
        self.geometry("250x250")

        self.configure(bg="#FFFFFF")


        # Поля для ввода данных клиента
        Label(self, text="Имя:").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        self.first_name_entry = Entry(self)
        self.first_name_entry.grid(row=0, column=1, pady=5, padx=5)

        Label(self, text="Фамилия:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
        self.last_name_entry = Entry(self)
        self.last_name_entry.grid(row=1, column=1, pady=5, padx=5)

        Label(self, text="Отчество:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
        self.middle_name_entry = Entry(self)
        self.middle_name_entry.grid(row=2, column=1, pady=5, padx=5)

        Label(self, text="Телефон:").grid(row=3, column=0, pady=5, padx=5, sticky="e")
        self.phone_entry = Entry(self)
        self.phone_entry.grid(row=3, column=1, pady=5, padx=5)

        Label(self, text="Адрес:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
        self.address_entry = Entry(self)
        self.address_entry.grid(row=4, column=1, pady=5, padx=5)

        # Кнопка для сохранения клиента
        Button(self, text="Сохранить", command=self.save_client).grid(row=5, column=0, columnspan=2, pady=10)

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

    def save_client(self):
        """Сохраняет нового клиента в базу данных."""
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        middle_name = self.middle_name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()

        if not first_name or not last_name or not phone or not address:
            messagebox.showerror("Ошибка", "Все поля, кроме отчества, обязательны для заполнения!")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO clients (first_name, last_name, middle_name, phone, address)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, middle_name, phone, address))
            self.conn.commit()
            messagebox.showinfo("Успех", "Клиент успешно добавлен!")
            self.refresh_callback()  # Обновляем таблицу клиентов
            self.destroy()
        except sqlite3.Error as e:
            self.conn.rollback()
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")