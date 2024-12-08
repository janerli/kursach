from database import add_user
from ct_db import delete_tables
import sqlite3

conn = sqlite3.connect('pizza.db')
# delete_tables(conn)
add_user(conn, 'janerli', 'meowmeow', 'admin')
add_user(conn, 'jan', 'meow', 'operator')
add_user(conn, 'anemia', 'pass', 'chef')