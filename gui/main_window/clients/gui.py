from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame


class Clients(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(bg = "#CEAB83")


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
        self.canvas.create_rectangle(
            42.0,
            95.0,
            907.0,
            666.0,
            fill="#D9D9D9",
            outline="")

        self.canvas.create_text(
            23.0,
            24.0,
            anchor="nw",
            text="Клиенты",
            fill="#000000",
            font=("Montserrat Alternates Bold", 36 * -1)
        )

