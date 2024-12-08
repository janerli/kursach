import tkinter as tk
from gui.login.gui import Login
from ct_db import create_tables
from database import conn
# from gui.main_window.main import mainWindow


root = tk.Tk()
root.withdraw()


if __name__ == "__main__":
    create_tables(conn)
    Login()
    root.mainloop()