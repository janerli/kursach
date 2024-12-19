import os
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame, messagebox, ttk
from tkinter.ttk import Treeview, Label

from tkcalendar import DateEntry
from PIL import Image, ImageTk

from database import get_revenue_by_period, get_top_3_pizzas, get_daily_revenue, conn

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Statistic(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)

        self.configure(bg = "#CEAB83")
        # Кэш для изображений
        self.image_cache = {}
        bn_style = ttk.Style()
        bn_style.configure('my1.TButton', font=('Montserrat Alternates', 20),
                            background='#CEAB83', foreground='black')

        # Создаём интерфейс
        self.create_widgets()
        self.load_statistics()

    def create_widgets(self):
        """Создаёт элементы интерфейса."""
        # Canvas для заголовка и оформления
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

        self.canvas.create_text(
            195.0,
            40.0,
            anchor="nw",
            text="Выручка",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        self.canvas.create_text(
            195.0,
            306.0,
            anchor="nw",
            text="Самые популярные пиццы:",
            fill="#000000",
            font=("Montserrat Alternates Regular", 36 * -1)
        )

        # Элементы для выбора периода
        Label(self, text="С:", font=('Montserrat Alternates', 20), background="#CEAB83").place(x=50, y=120)
        self.start_date_entry = DateEntry(self,
                                          width=10,
                                          height=40,
                                          background="#A37B54",  # Изменен цвет фона
                                          foreground="white",
                                          borderwidth=2,
                                          date_pattern='dd/mm/yyyy',
                                          font=('Montserrat Alternates', 10))
        self.start_date_entry.place(x=100, y=132)

        Label(self, text="По:", font=('Montserrat Alternates', 20), background="#CEAB83").place(x=250, y=120)
        self.end_date_entry = DateEntry(self,
                                        width=10,
                                        height=40,
                                        background="#A37B54",  # Изменен цвет фона
                                        foreground="white",
                                        borderwidth=2,
                                        date_pattern='dd/mm/yyyy',
                                        font = ('Montserrat Alternates', 10))
        self.end_date_entry.place(x=300, y=132)

        ttk.Button(self, text="Показать", command=self.update_revenue, style='my1.TButton').place(x=500, y=130)

        # Поле для отображения выручки
        self.revenue_label = Label(self, text="Выручка: 0.00 ₽", font=('Montserrat Alternates Bold', 24),
                                   background="#A37B54")
        self.revenue_label.place(x=60, y=170)


    def load_statistics(self):
        """Загружает данные для отображения."""
        # Загрузка ежедневной выручки
        daily_revenue = get_daily_revenue(conn)
        self.revenue_label.config(text=f"Выручка: {daily_revenue:.2f} ₽")

        # Загрузка популярных пицц
        self.load_top_pizzas()

    def load_top_pizzas(self):
        """Загружает топ-3 популярных пицц и отображает их в заданных позициях."""
        top_pizzas = get_top_3_pizzas(conn)

        # Координаты для расположения пицц
        positions = [
            (40, 420),  # Первая пицца
            (330, 420),  # Вторая пицца
            (630, 420),  # Третья пицца
        ]

        # Очистка предыдущих изображений
        self.image_cache = {}

        for i, pos in enumerate(positions):
            if i < len(top_pizzas):
                name, order_count = top_pizzas[i]
                x, y = pos

                # Название пиццы над картинкой
                self.canvas.create_text(
                    x + 130,
                    y - 50,
                    text=name,
                    fill="#000000",
                    font=('Montserrat Alternates Bold', 24),
                    anchor="n",
                )

                # Загружаем изображение пиццы
                image_path = self.get_pizza_image_path(name)
                if image_path:
                    if not os.path.exists(image_path):
                        messagebox.showerror("Ошибка", f"Изображение '{image_path}' не найдено.")
                        continue  # Переходим к следующей пицце
                    try:
                        img = Image.open(image_path).resize((250, 250), Image.LANCZOS)  # Увеличенный размер
                        img_tk = ImageTk.PhotoImage(img)
                        self.image_cache[name] = img_tk
                        self.canvas.create_image(x, y, anchor="nw", image=img_tk)
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Ошибка загрузки изображения '{image_path}': {e}")
                else:
                    messagebox.showerror("Ошибка", f"Путь к изображению для '{name}' не определен.")

                # Количество заказов под картинкой
                self.canvas.create_text(
                    x + 40,
                    y + 250,
                    text=f"{order_count} заказов",
                    fill="#000000",
                    font=('Montserrat Alternates', 12),
                    anchor="n",
                )
        self.update()

    def get_pizza_image_path(self, pizza_name):
        """Получает путь к изображению пиццы по её названию."""
        cursor = conn.cursor()
        cursor.execute("SELECT image_path FROM pizzas WHERE name = ?", (pizza_name,))
        result = cursor.fetchone()
        return result[0] if result else None

    def update_revenue(self):
        """Обновляет выручку за выбранный период."""
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        if start_date > end_date:
            messagebox.showerror("Ошибка", "Начальная дата не может быть позже конечной.")
            return

        revenue = get_revenue_by_period(conn, start_date, end_date)
        self.revenue_label.config(text=f"Выручка: {revenue:.2f} ₽")