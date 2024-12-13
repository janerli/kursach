from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, StringVar, Listbox, messagebox, END

from database import update_pizza_ingredients, get_pizza_ingredients, conn, add_ingredient_to_order, save_order

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class FinishOrder(Frame):
    def __init__(self, parent, user_id, delivery_type, address, order_items, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.configure(bg = "#CEAB83")
        self.parent = parent

        # Сохраненные данные
        self.user_id = user_id
        self.delivery_type = delivery_type
        self.address = address
        self.order_items = order_items
        self.selected_pizza = None

        # Переменные
        self.selected_ingredient = StringVar()


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
        #     19.0,
        #     105.0,
        #     484.0,
        #     328.0,
        #     fill="#D9D9D9",
        #     outline="") # first table

        self.canvas.create_rectangle(
            21.0,
            393.0,
            540.0,
            639.0,
            fill="#D9D9D9",
            outline="") # second table

        self.canvas.create_text(
            19.0,
            8.0,
            anchor="nw",
            text="Выберите пиццу для\nнастройки ингредиентов",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        self.pizza_listbox = Listbox(self, height=10, width=465)
        self.pizza_listbox.place(
            x=19.0,
            y=105.0,
            width=484.0,
            height=223.0)
        self.load_pizzas()

        self.canvas.create_text(
            22.0,
            333.0,
            anchor="nw",
            text="Ингредиенты:",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        self.ingredient_listbox = Listbox(self, height=10, width=519)
        self.ingredient_listbox.place(
            x=21.0,
            y=393.0,
            width=540.0,
            height=246.0
        )

        self.canvas.create_text(
            12.0,
            655.0,
            anchor="nw",
            text="Итоговая стоимость: 0 руб.",
            fill="#000000",
            font=("Montserrat Alternates Regular", 24 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        plus = Button(
            self.canvas,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_ingredient,
            relief="flat"
        )
        plus.place(
            x=641.0,
            y=473.0,
            width=57.04225540161133,
            height=54.0
        )

        # self.button_image_2 = PhotoImage(
        #     file=relative_to_assets("button_2.png"))
        # minus = Button(
        #     self.canvas,
        #     image=self.button_image_2,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: print("button_2 clicked"),
        #     relief="flat"
        # )
        # minus.place(
        #     x=734.0,
        #     y=473.0,
        #     width=57.04225540161133,
        #     height=54.0
        # )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        choose_btn = Button(
            self.canvas,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=self.select_pizza,
            relief="flat"
        )
        choose_btn.place(
            x=532.0,
            y=168.0,
            width=232.69927978515625,
            height=66.07679748535156
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        finish_btn = Button(
            self.canvas,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=self.finish_order,
            relief="flat"
        )
        finish_btn.place(
            x=700.0,
            y=622.0,
            width=232.69927978515625,
            height=66.07679748535156
        )

    def load_pizzas(self):
        """Загружает список пицц из текущего заказа."""
        for item in self.order_items:
            self.pizza_listbox.insert("end", f"{item['name']} (x{item['quantity']})")

    def select_pizza(self):
        """Выбирает пиццу для редактирования."""
        try:
            selected = self.pizza_listbox.curselection()
            if not selected:
                raise ValueError("Выберите пиццу из списка.")

            self.selected_pizza = self.order_items[selected[0]]
            self.load_ingredients()
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def load_ingredients(self):
        """Загружает ингредиенты выбранной пиццы."""
        try:
            self.ingredient_listbox.delete(0, END)
            ingredients = get_pizza_ingredients(conn)
            for ingredient in ingredients:
                self.ingredient_listbox.insert(END, ingredient["name"])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить ингредиенты: {e}")


    def add_ingredient(self):
        """Добавляет ингредиент в пиццу."""
        ingredient = self.ingredient_listbox.curselection()
        if not ingredient:
            messagebox.showerror("Ошибка", "Введите название ингредиента.")
            return

        try:
            add_ingredient_to_order(conn, self.selected_pizza["pizza_id"], ingredient)
            self.load_ingredients()
            messagebox.showinfo("Успех", "Ингредиент добавлен.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить ингредиент: {e}")


    def finish_order(self):
        """Завершает заказ."""
        save_order(conn, self.user_id, self.delivery_type, self.address, self.order_items)
        try:
            messagebox.showinfo("Успех", "Заказ успешно оформлен!")
            # self.destroy()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось завершить заказ: {e}")