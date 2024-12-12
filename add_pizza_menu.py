import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import database

class AddPizzaWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Добавить пиццу")
        self.geometry("300x350")

        self.name_label = ttk.Label(self, text="Название:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        self.description_label = ttk.Label(self, text="Описание:")
        self.description_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = ttk.Entry(self)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        self.price_label = ttk.Label(self, text="Цена:")
        self.price_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        self.image_path_label = ttk.Label(self, text="Путь к изображению:")
        self.image_path_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.image_path_entry = ttk.Entry(self)
        self.image_path_entry.grid(row=3, column=1, padx=5, pady=5)

        self.browse_button = ttk.Button(self, text="Обзор", command=self.browse_image)
        self.browse_button.grid(row=3, column=2, padx=5, pady=5)

        self.weight_label = ttk.Label(self, text="Вес:")
        self.weight_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.weight_entry = ttk.Entry(self)
        self.weight_entry.grid(row=4, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_pizza)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=10)

    def browse_image(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select an Image", filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("all files", "*.*")))
        self.image_path_entry.insert(0, filename)

    def add_pizza(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть числом.")
            return
        image_path = self.image_path_entry.get()
        try:
            weight = float(self.weight_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Вес должен быть числом.")
            return

        if database.create_pizza(database.conn, name, description, price, image_path, weight):
            messagebox.showinfo("Успех", "Пицца добавлена.")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Ошибка добавления пиццы.")


AddPizzaWindow(tk.Tk()).mainloop()