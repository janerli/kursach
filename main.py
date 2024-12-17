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

def center_window(root):
    """Центрирует окно на экране."""
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")



if __name__ == "__main__":
    # create_tables(conn)
    # Login()
    mainWindow(1)
    root.protocol("wm_delete_window", quit_me)
    center_window(root)
    root.mainloop()