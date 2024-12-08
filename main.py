import tkinter as tk
from gui.login.gui import loginWindow
from ct_db import create_tables, delete_tables
from database import conn
# from gui.admin_main.main import mainWindow


root = tk.Tk()
root.withdraw()
# добавить кнопку сменить пароль
# надпись кто зашел и должность

if __name__ == "__main__":

    create_tables(conn)
    loginWindow()
    root.mainloop()