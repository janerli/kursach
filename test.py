from database import add_user
import sqlite3

conn = sqlite3.connect('pizza.db')
add_user(conn, 'janerli', 'meowmeow', 'admin')