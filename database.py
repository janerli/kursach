import sqlite3
import bcrypt
import json
import logging
from functools import wraps

conn = sqlite3.connect('pizza.db')
DB_PATH = 'pizza.db'
# create_tables(conn)

def db_connection(func):
    """
    Декоратор для управления соединением с базой данных.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            logging.error(f"Ошибка в функции {func.__name__}: {e}")
            return None
        finally:
            conn.close()
    return wrapper

def add_user(conn, username, password, access_level_id, first_name=None, last_name=None, middle_name=None):
    """Добавляет нового пользователя."""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, access_level_id, first_name, last_name, middle_name)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, password, access_level_id, first_name, last_name, middle_name))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Пользователь '{username}' уже существует.")
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")



def get_user_by_username(conn, username):
    """Получает пользователя по имени."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()


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

def add_client(conn, first_name, last_name, middle_name, phone, address):
    """Добавляет клиента."""
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clients (first_name, last_name, middle_name, phone, address)
        VALUES (?, ?, ?, ?, ?)
    """, (first_name, last_name, middle_name, phone, address))
    conn.commit()



def get_pizza_price(conn, pizza_id):
    cursor = conn.cursor()
    cursor.execute("SELECT price FROM pizzas WHERE pizza_id = ?", (pizza_id,))
    price = cursor.fetchone()
    conn.close()
    return price[0] if price else None




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


# def get_pizzas(conn):
#     cursor = conn.cursor()
#     try:
#         cursor.execute("SELECT pizza_id, name, description, price, image_path, weight FROM pizzas")
#         pizzas = [dict(row) for row in
#                   cursor.fetchall()]
#         return pizzas
#     except sqlite3.OperationalError as e:
#         print(f"Ошибка получения списка пицц: {e}")
#         return []
#     except Exception as e:
#         print(f"Произошла ошибка: {e}")
#         return []

def get_pizzas(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT pizza_id, name, description, price, image_path, weight FROM pizzas")
        print("Запрос выполнен успешно.")  # Добавлен отладочный вывод
        rows = cursor.fetchall()
        print(f"Полученные данные: {rows}")  # Добавлен отладочный вывод
        columns = ['pizza_id', 'name', 'description', 'price', 'image_path', 'weight']
        pizzas = []
        for row in rows:
            if len(row) == len(columns):
                pizza = dict(zip(columns, row))
                pizzas.append(pizza)
            else:
                print(f"Неполная строка в таблице pizzas: {row}")
        return pizzas
    except sqlite3.OperationalError as e:
        print(f"Ошибка получения списка пицц: {e}")
        return None  # Вернем None, чтобы обработка в load_menu работала
    except Exception as e:
        print(f"Произошла ошибка в get_pizzas: {e}")  # Более конкретное сообщение
        return None


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


def get_order_history(conn, filters=None):
    """
    Возвращает историю заказов с применением фильтров.
    """
    conn.row_factory = sqlite3.Row
    filters = filters or {}
    query = """
        SELECT oh.history_id, oh.order_id, oh.client_id, oh.order_date, oh.total_price
        FROM order_history oh
        WHERE 1=1
    """
    params = []

    if "order_id" in filters:
        query += " AND oh.order_id = ?"
        params.append(filters["order_id"])
    if "client_id" in filters:
        query += " AND oh.client_id = ?"
        params.append(filters["client_id"])
    if "order_date" in filters:
        query += " AND oh.order_date = ?"
        params.append(filters["order_date"])
    if "total_price" in filters:
        query += " AND oh.total_price = ?"
        params.append(filters["total_price"])

    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Ошибка при получении истории заказов: {e}")
        return []


def get_pizza_ingredients(conn):
    """
    Получает список ингредиентов пиццы.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT ingredient_id, name, price FROM ingredients")
    columns = ['ingredient_id', 'name', 'quantity', 'price']
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def update_pizza_ingredients(conn, pizza_id, ingredient, action):
    """
    Добавляет или удаляет ингредиент пиццы.
    """
    cursor = conn.cursor()
    if action == "add":
        cursor.execute("INSERT INTO ingredients (pizza_id, name) VALUES (?, ?)", (pizza_id, ingredient))
    elif action == "remove":
        cursor.execute("DELETE FROM ingredients WHERE pizza_id = ? AND name = ?", (pizza_id, ingredient))
    else:
        raise ValueError("Недопустимое действие.")

def save_order(conn, client_id, delivery, status, order_items):
    """
    Сохраняет заказ в базу данных, включая элементы заказа и дополнительные ингредиенты.
    """
    cursor = conn.cursor()
    try:
        # Сохраняем основной заказ
        cursor.execute("""
            INSERT INTO orders (client_id, delivery, status)
            VALUES (?, ?, ?)
        """, (client_id, delivery, status))
        order_id = cursor.lastrowid

        # Сохраняем элементы заказа
        for item in order_items:
            # Собираем список добавленных ингредиентов
            additional_ingredients = ",".join(item.get("additional_ingredients", []))
            cursor.execute("""
                INSERT INTO order_items (order_id, pizza_id, quantity, additional_ingredients)
                VALUES (?, ?, ?, ?)
            """, (order_id, item["pizza_id"], item["quantity"], additional_ingredients))

        conn.commit()
        print(f"Заказ #{order_id} успешно сохранен.")
        return order_id
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Ошибка сохранения заказа: {e}")
        return None


def add_ingredient_to_order(conn, order_item_id, ingredient_name):
    """
    Добавляет ингредиент в заказ (к текущему элементу заказа).
    """
    cursor = conn.cursor()
    try:
        # Проверяем, существует ли этот ингредиент
        cursor.execute("SELECT ingredient_id FROM ingredients WHERE name = ?", (ingredient_name,))
        ingredient = cursor.fetchone()

        if ingredient:
            ingredient_id = ingredient[0]
            cursor.execute("SELECT additional_ingredients FROM order_items WHERE order_item_id = ?", (order_item_id,))
            existing_ingredients = cursor.fetchone()[0]

            # Если ингредиенты уже есть, добавляем новый
            if existing_ingredients:
                updated_ingredients = f"{existing_ingredients},{ingredient_name}"
            else:
                updated_ingredients = ingredient_name

            # Обновляем строку ингредиентов
            cursor.execute("""
                UPDATE order_items
                SET additional_ingredients = ?
                WHERE order_item_id = ?
            """, (updated_ingredients, order_item_id))

            conn.commit()
            print(f"Ингредиент '{ingredient_name}' успешно добавлен.")
        else:
            print(f"Ингредиент '{ingredient_name}' не найден.")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Ошибка при добавлении ингредиента в заказ: {e}")

def create_ingredient(conn, name, quantity, unit, price):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ingredients (name, quantity, unit, price) VALUES (?, ?, ?, ?)", (name, quantity, unit, price))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # Обработка уникальности имени
        conn.rollback()
        return False
    except Exception as e:
        conn.rollback()
        print(f"Ошибка добавления ингредиента: {e}")
        return False

def update_order_status(conn, order_id, new_status):
    """
    Обновляет статус заказа.
    """
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))

def move_order_to_history(conn, order_id):
    """
    Перемещает заказ в таблицу order_history.
    """
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO order_history (order_id, client_id, order_date, total_price)
        SELECT order_id, client_id, DATE('now'), total_price
        FROM orders
        WHERE order_id = ?
    """, (order_id,))
    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))

def get_all_orders(conn):
    """
    Возвращает список всех заказов.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, delivery, status FROM orders")
    return cursor.fetchall()

def get_order_details(conn, order_id):
    """
    Получает детали заказа из таблицы order_items по order_id.
    :param conn: Соединение с базой данных.
    :param order_id: Идентификатор заказа.
    :return: Список строк с деталями заказа.
    """
    cursor = conn.cursor()
    cursor.execute("""
        SELECT order_item_id, pizza_id, quantity, additional_ingredients
        FROM order_items
        WHERE order_id = ?
    """, (order_id,))
    return cursor.fetchall()





