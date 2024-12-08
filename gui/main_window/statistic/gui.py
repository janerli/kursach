from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Frame


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class Statistic(Frame):
window = Tk()

window.geometry("948x700")
window.configure(bg = "#CEAB83")


canvas = Canvas(
    window,
    bg = "#CEAB83",
    height = 700,
    width = 948,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    35.0,
    411.0,
    280.0,
    642.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    332.0,
    411.0,
    577.0,
    642.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    629.0,
    411.0,
    874.0,
    642.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    35.0,
    98.0,
    548.0,
    274.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    195.0,
    40.0,
    anchor="nw",
    text="Выручка",
    fill="#000000",
    font=("MontserratAlternates Regular", 36 * -1)
)

canvas.create_text(
    195.0,
    306.0,
    anchor="nw",
    text="Самые популярные пиццы:",
    fill="#000000",
    font=("MontserratAlternates Regular", 36 * -1)
)
window.resizable(False, False)
window.mainloop()
