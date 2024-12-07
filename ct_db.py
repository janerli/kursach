import sqlite3

def delete_tables(conn):
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS users''')
    cursor.execute('''DROP TABLE IF EXISTS clients''')
    cursor.execute('''DROP TABLE IF EXISTS pizzas''')
    cursor.execute('''DROP TABLE IF EXISTS ingredients''')
    cursor.execute('''DROP TABLE IF EXISTS orders''')
    cursor.execute('''DROP TABLE IF EXISTS order_history''')
    cursor.execute('''DROP TABLE IF EXISTS order_items''')

    conn.commit()

def create_tables(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                access_level INTEGER NOT NULL CHECK (access_level IN ('admin', 'operator', 'chef'))
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                middle_name TEXT,
                phone TEXT,
                address TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pizzas (
                pizza_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                image_path TEXT,
                weight REAL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)

        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        delivery TEXT NOT NULL CHECK (delivery IN ('доставка', 'самовывоз')),
                        status TEXT NOT NULL CHECK (status IN ('новый', 'в работе', 'готов', 'завершен', 'отменен'))
                    )
                """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                client_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients(client_id),
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                pizza_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                additional_ingredients TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (pizza_id) REFERENCES pizzas(pizza_id)
            )
        """)

        conn.commit()
        print("Таблицы созданы успешно.")
    except sqlite3.OperationalError as e:
        conn.rollback()
        print(f"Ошибка создания таблиц: {e}")
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка: {e}")