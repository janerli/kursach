import tkinter as tk
from gui.login.gui import loginWindow
from ct_db import create_tables
from database import conn
# from gui.main_window.main import mainWindow

# Main window constructor
root = tk.Tk()  # Make temporary window for app to start
root.withdraw()  # WithDraw the window


if __name__ == "__main__":
    create_tables(conn)
    loginWindow()
    root.mainloop()