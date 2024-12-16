import tkinter as tk
from gui.login.gui import Login
from ct_db import create_tables
from database import conn
from gui.main_window.main import mainWindow

# from gui.main_window.main import mainWindow


root = tk.Tk()
root.withdraw()
def quit_me():

    root.quit()
    root.destroy()


if __name__ == "__main__":
    create_tables(conn)
    Login()
    #mainWindow(1)
    quit_me()
    root.mainloop()