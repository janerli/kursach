import sqlite3
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, IntVar, ttk, messagebox, Label

from database import get_pizzas, conn

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

        # Переменные
        self.selected_pizza_id = IntVar()
        self.quantity = IntVar(value=1)
        self.order_items = []  # Список {pizza_id, quantity, name, price}
        self.total_price = 0

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

        style = ttk.Style()
        style.configure('mystyle4.Treeview', font=('Montserrat Alternates', 9))
        style.configure('mystyle4.Treeview.Heading',
                        background='#715E48',
                        font=('Montserrat Alternates Bold', 11),
                        foreground='black')

        self.menu_table = ttk.Treeview(self.canvas, columns=["id", "name", "price"], show="headings", height=10,
                                       style='mystyle4.Treeview')
        self.menu_table.heading("id", text="ID")
        self.menu_table.heading("name", text="Название")
        self.menu_table.heading("price", text="Цена")
        self.menu_table.column("id", width=50, anchor="center")
        self.menu_table.column("name", width=400, anchor="w")
        self.menu_table.column("price", width=100, anchor="center")
        self.menu_table.place(x=22.0,
            y=78.0,
            width=891.0,
            height=197.0,)
        self.load_menu()

        self.order_table = ttk.Treeview(self.canvas, columns=["name", "quantity", "price"],
                                        show="headings", height=5, style='mystyle4.Treeview')
        self.order_table.heading("name", text="Название")
        self.order_table.heading("quantity", text="Количество")
        self.order_table.heading("price", text="Цена")
        self.order_table.column("name", width=400, anchor="w")
        self.order_table.column("quantity", width=100, anchor="center")
        self.order_table.column("price", width=100, anchor="center")
        self.order_table.place(
            x = 22.0,
            y = 408.0,
            width=869.0,
            height=210.0
        )


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

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        plus = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_pizza,
            relief="flat"
        )
        plus.place(
            x=660.0,
            y=280.0,
            width=73.94366455078125,
            height=70.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        minus = Button(
            self.canvas,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.remove_pizza,
            relief="flat"
        )
        minus.place(
            x=780.5556640625,
            y=280.0,
            width=73.94366455078125,
            height=70.0
        )

        # self.canvas.create_text(
        #     21.0,
        #     653.0,
        #     anchor="nw",
        #     text="Итоговая стоимость: 0 руб.",
        #     fill="#000000",
        #     font=("Montserrat Alternates Regular", 24 * -1)
        # )

        self.total_label = Label(
            self.canvas,
            text="Итоговая стоимость: 0 руб.",
            font=("Montserrat Alternates Regular", 24),
            bg="#CEAB83")
        self.total_label.place(x=21.0, y=653.0)

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        next_btn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.next_step(),
            relief="flat"
        )
        next_btn.place(
            x=749.0,
            y=631.0,
            width=193.17681884765625,
            height=54.85408401489258
        )

    def load_menu(self):
        """Загружает данные меню из базы."""
        try:
            pizzas = get_pizzas(conn=sqlite3.connect('pizza.db'))
            for pizza in pizzas:
                self.menu_table.insert("", "end", values=(pizza["pizza_id"], pizza["name"], pizza["price"]))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить меню: {e}")

    def add_pizza(self):
        """Добавляет выбранную пиццу в текущий заказ."""
        try:
            selected_item = self.menu_table.selection()
            if not selected_item:
                raise ValueError("Выберите пиццу из меню.")

            pizza_id, name, price = self.menu_table.item(selected_item[0], "values")
            pizza_id = int(pizza_id)
            price = float(price)

            # Проверяем, есть ли пицца уже в заказе
            for item in self.order_items:
                if item["pizza_id"] == pizza_id:
                    item["quantity"] += 1
                    break
            else:
                self.order_items.append({"pizza_id": pizza_id, "name": name, "price": price, "quantity": 1})

            self.update_order()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def remove_pizza(self):
        """Удаляет выбранную пиццу из текущего заказа."""
        try:
            selected_item = self.order_table.selection()
            if not selected_item:
                raise ValueError("Выберите пиццу из текущего заказа.")

            name, quantity, price = self.order_table.item(selected_item[0], "values")
            quantity = int(quantity)
            price = float(price)

            # Находим элемент в self.order_items по имени
            for item in self.order_items:
                if item["name"] == name:
                    item["quantity"] -= 1
                    self.total_price -= price
                    if item["quantity"] == 0:
                        self.order_items.remove(item)
                    break
            else:
                raise ValueError("Пицца не найдена в заказе.")

            self.update_order()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
        except IndexError as e:
            messagebox.showerror("Ошибка", "Неверные данные в таблице заказа.")

    def update_order(self):
        """Обновляет таблицу текущего заказа и итоговую стоимость."""
        for item in self.order_table.get_children():
            self.order_table.delete(item)

        self.total_price = 0
        for item in self.order_items:
            self.total_price += item["price"] * item["quantity"]
            self.order_table.insert("", "end",
                                    values=(item["name"], item["quantity"], item["price"] * item["quantity"]))

        self.total_label.config(text=f"Итоговая стоимость: {self.total_price} руб.")

    def next_step(self):
        """Переход к следующему этапу."""
        if not self.order_items:
            messagebox.showerror("Ошибка", "Заказ не может быть пустым!")
            return

        # Закрываем текущее окно
        from database import save_order_with_items
        try:
            # Сохраняем заказ в базу данных
            order_id = save_order_with_items(
                client_id=self.user_id,
                order_date=datetime.now(),
                total_price=self.total_price,
                delivery='доставка',
                status="новый",
                items=self.order_items
            )
            self.parent.navigate("finish", order_id, self.user_id, self.delivery_type, self.address,
                                 self.order_items, self.total_price)
            self.place_forget()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить заказ: {e}")


        # Переход к следующему этапу
        # AdditionalSettingsWindow(self.user_id, self.delivery_type, self.address, self.order_items)

