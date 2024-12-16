import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import database

class AddIngredientWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Добавить ингредиент")
        self.geometry("350x250")

        self.name_label = ttk.Label(self, text="Название:")
        self.name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)



        self.price_label = ttk.Label(self, text="Цена:")
        self.price_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self, text="Добавить", command=self.add_ingredient)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

    def add_ingredient(self):
        name = self.name_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Цена должна быть числом.")
            return

        if database.create_ingredient(database.conn, name, price):
            messagebox.showinfo("Успех", "Ингредиент добавлен.")
            self.destroy()
        else:
            messagebox.showerror("Ошибка", "Ошибка добавления ингредиента.")

AddIngredientWindow(tk.Tk()).mainloop()