
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar, messagebox, ttk
from tkinter.ttk import Treeview

from database import get_order_history, conn

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class OrderHistory(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg = "#CEAB83")

        self.filters = {
            "order_id": StringVar(),
            "client_id": StringVar(),
            "order_date": StringVar(),
            "total_price": StringVar()
        }
        self.sort_column = None
        self.sort_order = "ASC"

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
        # self.canvas.create_rectangle(
        #     21.0,
        #     161.0,
        #     927.0,
        #     631.0,
        #     fill="#D9D9D9",
        #     outline="")

        style = ttk.Style()
        style.configure('mystyle3.Treeview', rowheight=30, font=('Montserrat Alternates', 9))
        style.configure('mystyle3.Treeview.Heading',
                        background='#715E48',
                        font=('Montserrat Alternates Bold', 11),
                        foreground='black')

        self.tree = Treeview(self, columns=("order_id", "client_id", "order_date", "total_price"),
                             show="headings", style='mystyle3.Treeview')
        self.tree.heading("order_id", text="ID заказа", command=lambda: self.sort_by("order_id"))
        self.tree.heading("client_id", text="ID клиента", command=lambda: self.sort_by("client_id"))
        self.tree.heading("order_date", text="Дата заказа", command=lambda: self.sort_by("order_date"))
        self.tree.heading("total_price", text="Итоговая цена", command=lambda: self.sort_by("total_price"))
        self.tree.column("order_id", width=100, anchor="center")
        self.tree.column("client_id", width=100, anchor="center")
        self.tree.column("order_date", width=200, anchor="center")
        self.tree.column("total_price", width=150, anchor="center")
        self.tree.place(x=21.0, y=161.0, width=906.0, height=470.0)
        self.refresh_data()

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        update_btn = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.refresh_data,
            relief="flat"
        )
        update_btn.place(
            x=830.0,
            y=633.7333984375,
            width=70.0,
            height=66.26666259765625
        )

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            234.5,
            49.0,
            image=self.entry_image_1
        )
        order_en = Entry(
            self.canvas,
            textvariable=self.filters['order_id'],
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Montserrat Alternates Regular", 24 * -1)
        )
        order_en.place(
            x=170.0,
            y=26.0,
            width=129.0,
            height=44.0
        )

        self.entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = self.canvas.create_image(
            671.5,
            117.0,
            image=self.entry_image_2
        )
        total_en = Entry(
            self.canvas,
            textvariable=self.filters['total_price'],
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Montserrat Alternates Regular", 24 * -1)
        )
        total_en.place(
            x=607.0,
            y=94.0,
            width=129.0,
            height=44.0
        )

        self.entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        entry_bg_3 = self.canvas.create_image(
            671.5,
            49.0,
            image=self.entry_image_3
        )
        date_en = Entry(
            self.canvas,
            textvariable=self.filters['order_date'],
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Montserrat Alternates Regular", 24 * -1)
        )
        date_en.place(
            x=607.0,
            y=26.0,
            width=129.0,
            height=44.0
        )

        self.entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = self.canvas.create_image(
            234.5,
            117.0,
            image=self.entry_image_4
        )
        client_en = Entry(
            self.canvas,
            bd=0,
            bg="#D9D9D9",
            fg="#000716",
            highlightthickness=0,
            font=("Montserrat Alternates Regular", 24 * -1),
        )
        client_en.place(
            x=170.0,
            y=94.0,
            width=129.0,
            height=44.0
        )

        self.canvas.create_text(
            21.0,
            37.0,
            anchor="nw",
            text="ID заказа",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.canvas.create_text(
            402.0,
            37.0,
            anchor="nw",
            text="Дата заказа",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.canvas.create_text(
            402.0,
            105.0,
            anchor="nw",
            text="Итоговая сумма",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.canvas.create_text(
            21.0,
            105.0,
            anchor="nw",
            text="ID клиента",
            fill="#000000",
            font=("Montserrat Alternates Regular", 20 * -1)
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        filter_btn = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.apply_filters,
            relief="flat"
        )
        filter_btn.place(
            x=786.0,
            y=20.0,
            width=158.0,
            height=120.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        delete_btn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        delete_btn.place(
            x=672.0,
            y=633.7333984375,
            width=70.0,
            height=66.26666259765625
        )

    def refresh_data(self):
        """Обновляет данные в таблице."""
        try:
            # Получаем все записи без фильтров
            data = get_order_history(conn)
            self.populate_table(data)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def apply_filters(self):
        """Применяет фильтры к данным."""
        try:
            # Собираем фильтры
            applied_filters = {key: var.get().strip() for key, var in self.filters.items() if var.get().strip()}

            # Получаем отфильтрованные данные
            data = get_order_history(conn, filters=applied_filters)
            self.populate_table(data)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось применить фильтры: {e}")

    def sort_by(self, column):
        """Сортирует данные по выбранной колонке."""
        if self.sort_column == column:
            # Если колонка уже используется для сортировки, меняем порядок
            self.sort_order = "DESC" if self.sort_order == "ASC" else "ASC"
        else:
            # Новая колонка для сортировки
            self.sort_column = column
            self.sort_order = "ASC"

        self.apply_filters()  # Повторно применяем фильтры с сортировкой

    def populate_table(self, data):
        """Заполняет таблицу данными."""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Сортируем данные
        if self.sort_column:
            data.sort(key=lambda row: row[self.sort_column], reverse=(self.sort_order == "DESC"))

        # Добавляем записи
        for row in data:
            self.tree.insert("", "end",
                             values=(row["order_id"], row["client_id"], row["order_date"], row["total_price"]))

