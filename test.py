from database import add_user
import sqlite3

conn = sqlite3.connect('pizza.db')
cursor = conn.cursor()
add_user(conn, 'admin', 'admin', 1)

