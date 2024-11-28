import sqlite3
import bcrypt
import json
# from ct_db import create_tables

conn = sqlite3.connect('pizza.db')
# create_tables(conn)


def add_user(conn, username, password, access_level):
    cursor = conn.cursor()
    try:
        # Проверка на существование пользователя
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cursor.fetchone() is not None:
            return False  # Пользователь с таким именем уже существует

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute("INSERT INTO users (username, password, access_level) VALUES (?, ?, ?)",
                       (username, hashed_password, access_level))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"Ошибка добавления пользователя: {e}")
        return False
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка: {e}")
        return False


def get_user_by_username(conn, username):  # Подключение к базе данных
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user


def check_login(conn, username, password):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return user['user_id'], user['access_level']
    else:
        return None, None


def create_order(conn, client_id, order_items):
    cursor = conn.cursor()
    try:
        conn.execute("BEGIN TRANSACTION")
        total_price = sum(item['quantity'] * get_pizza_price(item['pizza_id']) for item in order_items)
        cursor.execute(
            "INSERT INTO orders (client_id, order_date, total_price, status) VALUES (?, datetime('now'), ?, 'new')",
            (client_id, total_price))
        order_id = cursor.lastrowid
        for item in order_items:
            cursor.execute("INSERT INTO order_items (order_id, pizza_id, quantity) VALUES (?, ?, ?)",
                           (order_id, item['pizza_id'], item['quantity']))
        conn.commit()
        return order_id
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"Ошибка целостности данных: {e}")
        return None
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка: {e}")
        return None
    finally:
        conn.close()


def get_pizza_price(conn, pizza_id):
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM pizzas WHERE pizza_id = ?", (pizza_id,))
    price = cursor.fetchone()
    conn.close()
    return price[0] if price else None


def get_order(conn, order_id):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, client_id, order_date, total_price, status FROM orders WHERE order_id = ?",
                   (order_id,))
    order_data = cursor.fetchone()
    if order_data is None:
        return None

    order = {
        'order_id': order_data['order_id'],
        'client_id': order_data['client_id'],
        'order_date': order_data['order_date'],
        'total_price': order_data['total_price'],
        'status': order_data['status']
    }

    cursor.execute("SELECT pizza_id, quantity FROM order_items WHERE order_id = ?", (order_id,))
    order_items = cursor.fetchall()
    order['items'] = [{'pizza_id': item['pizza_id'], 'quantity': item['quantity']} for item in order_items]

    return order


def update_order(conn, order_id, updates):
    cursor = conn.cursor()
    try:
        set_query = ", ".join([f"{key} = ?" for key in updates])
        query = f"UPDATE orders SET {set_query} WHERE order_id = ?"
        values = list(updates.values()) + [order_id]
        cursor.execute(query, values)
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        print(f"Ошибка обновления заказа: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def delete_order(conn, order_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM orders WHERE order_id = ?", (order_id,))
        if cursor.fetchone() is None:
            return False  # Заказ не найден

        conn.execute("BEGIN TRANSACTION")

        # Удаление записей из order_items
        cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))

        # Удаление записи из orders
        cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))

        conn.commit()  # Завершение транзакции
        return True
    except sqlite3.OperationalError as e:
        conn.rollback()  # Отмена транзакции при ошибке
        print(f"Ошибка удаления заказа: {e}")
        return False
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка: {e}")
        return False


def get_pizzas(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT pizza_id, name, description, price, image_path, weight FROM pizzas")
        pizzas = [dict(row) for row in
                  cursor.fetchall()]
        return pizzas
    except sqlite3.OperationalError as e:
        print(f"Ошибка получения списка пицц: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def get_pizza_by_id(conn, pizza_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT pizza_id, name, description, price, image_path, weight FROM pizzas WHERE pizza_id = ?",
                       (pizza_id,))
        pizza = cursor.fetchone()
        return dict(pizza) if pizza else None
    except sqlite3.OperationalError as e:
        print(f"Ошибка получения информации о пицце: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def create_pizza(conn, name, description, price, image_path, weight):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO pizzas (name, description, price, image_path, weight) VALUES (?, ?, ?, ?, ?)",
                       (name, description, price, image_path, weight))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Ошибка: Пицца с таким именем уже существует: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка при создании пиццы: {e}")
        return False


def delete_pizza(conn, pizza_id):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pizzas WHERE pizza_id = ?", (pizza_id,))
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        print(f"Ошибка удаления пиццы: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def get_clients(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT client_id, name, phone, address FROM clients")
        clients = [dict(row) for row in cursor.fetchall()]
        return clients
    except sqlite3.OperationalError as e:
        print(f"Ошибка получения списка клиентов: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def get_client_by_id(conn, client_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT client_id, name, phone, address FROM clients WHERE client_id = ?", (client_id,))
        client = cursor.fetchone()
        return dict(client) if client else None
    except sqlite3.OperationalError as e:
        print(f"Ошибка получения информации о клиенте: {e}")
        return None
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


def create_client(conn, name, phone, address):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clients (name, phone, address) VALUES (?, ?, ?)", (name, phone, address))
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Ошибка: Клиент с таким телефоном уже существует: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка при создании клиента: {e}")
        return False


def update_client(conn, client_id, updates):
    cursor = conn.cursor()
    try:
        set_query = ", ".join([f"{key} = ?" for key in updates])
        query = f"UPDATE clients SET {set_query} WHERE client_id = ?"
        values = list(updates.values()) + [client_id]
        cursor.execute(query, values)
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        print(f"Ошибка обновления клиента: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def delete_client(conn, client_id):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM orders WHERE client_id = ?", (client_id,))
        if cursor.fetchone() is not None:
            return False  # У клиента есть заказы

        cursor.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
        conn.commit()
        return True
    except sqlite3.OperationalError as e:
        print(f"Ошибка удаления клиента: {e}")
        return False
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return False


def get_daily_revenue(conn):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT SUM(total_price) FROM orders WHERE strftime('%Y-%m-%d', order_date) = strftime('%Y-%m-%d', 'now')"
        )
        revenue = cursor.fetchone()[0]
        return revenue if revenue is not None else 0.0
    except sqlite3.OperationalError as e:
        print(f"Ошибка получения выручки: {e}")
        return 0.0
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return 0.0


def get_top_3_pizzas(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT p.name, COUNT(oi.pizza_id) AS order_count
            FROM pizzas p
            JOIN order_items oi ON p.pizza_id = oi.pizza_id
            GROUP BY p.name
            ORDER BY order_count DESC
            LIMIT 3
        """)
        top_pizzas = cursor.fetchall()
        return top_pizzas
    except sqlite3.OperationalError as e:
        print(f"Ошибка получения топ-3 пицц: {e}")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []
