from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage, Toplevel, Frame, StringVar, messagebox, \
    Label, ttk
from tkinter.ttk import Scrollbar, Combobox, Treeview

import user_session
from database import update_order_status, move_order_to_history, get_all_orders, conn, get_order_details

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class ViewOrder(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.access_level = user_session.session.get_access_level()
        self.configure(bg="#CEAB83")



        self.canvas = Canvas(
            self,
            bg="#CEAB83",
            height=700,
            width=948,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(
            20.0,
            77.0,
            926.0,
            594.0,
            fill="#D9D9D9",
            outline="")

        style = ttk.Style()
        style.configure('mystyle1.Treeview', rowheight=30, font=('Montserrat Alternates', 13))
        style.configure('mystyle1.Treeview.Heading',
                         background='#715E48',
                         font=('Montserrat Alternates Bold', 15),
                         foreground='black')

        self.tree = Treeview(self, columns=("order_id", "delivery", "status"), show="headings", style='mystyle1.Treeview')
        self.tree.heading("order_id", text="ID Заказа")
        self.tree.heading("delivery", text="Тип доставки")
        self.tree.heading("status", text="Статус")
        self.load_data()

        # Прокрутка для таблицы
        scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.place(x=20, y=77, width=906, height=517)
        scrollbar.place(x=926, y=77, width=17, height=517)

        self.tree.bind("<Double-1>", self.open_order_details)



        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("add"),
            relief="flat"
        )
        button_1.place(
            x=650.0,
            y=612.0,
            width=285.0,
            height=71.0
        )

        self.canvas.create_text(
            20.0,
            19.0,
            anchor="nw",
            text="Заказы",
            fill="#000000",
            font=("Montserrat Alternates Bold", 36 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        delete_button = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.delete_selected,
            relief="flat"
        )
        delete_button.place(
            x=546.0,
            y=614.0,
            width=73.94366455078125,
            height=70.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        update_btn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.load_data,
            relief="flat"
        )
        update_btn.place(
            x=461.0,
            y=614.0,
            width=73.94000244140625,
            height=70.0
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        edit_btn = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.open_status_window,
            relief="flat"
        )
        edit_btn.place(
            x=25.0,
            y=614.0,
            width=311.0,
            height=71.0
        )

        if self.access_level == 3:
            delete_button.place_forget()
            button_1.place_forget()

    def load_data(self):
        """Загружает данные из базы в таблицу."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            orders = get_all_orders(conn)  # Вызов функции из database.py
            for order in orders:
                self.tree.insert("", "end", values=order)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def open_status_window(self):

        """Открывает окно изменения статуса заказа."""
        def center_window(root):
            """Центрирует окно на экране."""
            root.update_idletasks()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            window_width = root.winfo_width()
            window_height = root.winfo_height()
            title_bar_height = 70
            y = (screen_height - window_height - title_bar_height) // 2
            x = (screen_width - window_width) // 2
            root.geometry(f"+{x}+{y}")

        status_window = Toplevel(self)
        status_window.iconphoto(False, PhotoImage(file="gui/icon.png"))
        status_window.title("Изменить статус заказа")
        status_window.geometry("300x200")
        center_window(status_window)
        status_window.configure(background="#f0f4fc")

        Label(status_window, text="Номер заказа:", background='#f0f4fc', foreground='black',
              font=('Montserrat Alternates', 11)).pack(pady=10)
        order_id_var = StringVar()
        ttk.Entry(status_window, textvariable=order_id_var).pack()

        Label(status_window, text="Новый статус:", background='#f0f4fc', foreground='black',
              font=('Montserrat Alternates', 11)).pack(pady=10)
        status_var = StringVar()
        status_combobox = Combobox(status_window, values=["новый", "в работе", "готов", "завершен", "отменен"],
                                   state="readonly")
        status_combobox.pack()

        def save_status():
            order_id = order_id_var.get()
            new_status = status_combobox.get()

            if not order_id.isdigit():
                messagebox.showerror("Ошибка", "Номер заказа должен быть числом!")
                return

            if not new_status:
                messagebox.showerror("Ошибка", "Выберите новый статус!")
                return

            try:
                # Обновляем статус заказа
                update_order_status(conn, order_id=order_id, new_status=new_status)

                # Перемещаем в историю, если необходимо
                if new_status in ["завершен", "отменен"]:
                    move_order_to_history(conn,order_id=order_id)

                messagebox.showinfo("Успех", f"Статус заказа {order_id} обновлен!")
                self.load_data()
                status_window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось обновить статус: {e}")


        stl = ttk.Style()
        stl.configure('my1.TButton', font=('Montserrat Alternates Bold', 11),
                      background='#f0f4fc', foreground='black',
                      height=15, anchor='center', padding=[1, 1])
        ttk.Button(status_window, text="Сохранить", command=save_status, style='my1.TButton').pack(pady=10)

    def delete_selected(self):
        """Удаляет выбранную строку из базы данных и обновляет таблицу."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите строку для удаления!")
            return

        # Получаем ID выбранного заказа
        order_id = self.tree.item(selected_item, "values")[0]

        try:
            # Удаляем запись из базы данных
            from database import delete_order  # Импорт функции для удаления
            delete_order(conn, order_id=order_id)

            # Обновляем таблицу
            self.load_data()
            messagebox.showinfo("Успех", f"Заказ с ID {order_id} успешно удален!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить заказ: {e}")

    def open_order_details(self, event):
        """Открывает окно с подробностями заказа."""
        def center_window(root):
            """Центрирует окно на экране."""
            root.update_idletasks()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            window_width = root.winfo_width()
            window_height = root.winfo_height()
            title_bar_height = 70
            y = (screen_height - window_height - title_bar_height) // 2
            x = (screen_width - window_width) // 2
            root.geometry(f"+{x}+{y}")

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Ошибка", "Выберите строку для просмотра деталей!")
            return

        # Получаем ID заказа
        order_id = self.tree.item(selected_item, "values")[0]

        # Создаем окно с деталями заказа
        details_window = Toplevel(self)
        details_window.title(f"Детали заказа {order_id}")
        center_window(details_window)
        details_window.geometry("700x300")
        details_window.iconphoto(False, PhotoImage(file="gui/icon.png"))


        # Создаем Treeview для отображения деталей заказа

        details_tree = Treeview(details_window,
                                columns=("order_item_id", "pizza_id", "quantity", "additional_ingredients"),
                                show="headings", style='mystyle1.Treeview')
        details_tree.heading("order_item_id", text="ID Элемента")
        details_tree.heading("pizza_id", text="ID Пиццы")
        details_tree.heading("quantity", text="Количество")
        details_tree.heading("additional_ingredients", text="Доп. Ингредиенты")

        # Прокрутка для дерева
        details_scrollbar = Scrollbar(details_window, orient="vertical", command=details_tree.yview)
        details_tree.configure(yscroll=details_scrollbar.set)
        details_tree.column("#1", width=100)
        details_tree.column("#2", width=100)
        details_tree.column("#3", width=100)
        details_tree.column("#4", width=100)
        details_tree.grid(row=0, column=0, sticky="nsew")
        details_scrollbar.grid(row=0, column=1, sticky="ns")

        # Загрузка данных о заказе с использованием функции из database.py
        try:
            rows = get_order_details(conn, order_id=order_id)
            print("Детали заказа:", rows)  # Для отладки
            for row in rows:
                details_tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить детали заказа: {e}")

        # Кнопка закрытия окна
        ttk.Button(details_window, text="Закрыть", command=details_window.destroy).grid(row=1, column=0, pady=10)

        details_window.columnconfigure(0, weight=1)
        details_window.rowconfigure(0, weight=1)

