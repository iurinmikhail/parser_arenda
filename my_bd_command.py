import sqlite3
import datetime


def create_table():
    """Создание базы данных"""
    with sqlite3.connect("arenda_bd.db") as db:
        cursor = db.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS arenda(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_card INT,
        title TEXT,
        price TEXT,
        etaj TEXT,
        square TEXT,
        zone TEXT,
        address TEXT,
        description TEXT,
        url TEXT,
        publish_date TEXT,
        parsing_date DATE
        );""")
        db.commit()


def insert_arenda(col1, col2, col3, col4, col5, col6, col7, col8, col9, col10):
    """Вставляет данные в бд"""
    with sqlite3.connect("arenda_bd_saved_with_sqlite.db") as db:
        cursor = db.cursor()
        data_list = (col1, col2, col3, col4,col5, col6, col7, col8, col9, col10, datetime.datetime.now())
        cursor.execute("""
                        INSERT INTO news (id_card, title, price, etaj, square, zone, address, description,/
                        url, publish_date, parsing_date) 
                        VALUES (?, ?, ?, ?, ?);
                            """, data_list)
        db.commit()


def check_news(title):
    """Проверка наличия объявления в БД"""
    with sqlite3.connect("arenda_bd_saved_with_sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT title FROM arenda WHERE title = ? """, (title,))
        result = cursor.fetchall()
        if len(result) == 0:
            return 0
        else:
            return 1


def get_data_from_db():
    """Получение данных из БД"""
    with sqlite3.connect("arenda_bd_saved_with_sqlite.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT id_card, title, price, etaj, square, zone, address, description,/
                        url, publish_date, parsing_date FROM arenda""")
        # вывод всех объявлений
        data_set = cursor.fetchall()
        return data_set