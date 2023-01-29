import sqlite3 as sq
from datetime import datetime
from sqlite3 import Error

from tqdm import tqdm

class CommandSQlite:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = self._create_connection()

    def _create_connection(self):
        connection = None
        try:
            with sq.connect(self.db_path) as connection:
                print(f"Подключился к базе данных {self.db_path} ")
        except Error as e:
            print(f"Произошла ошибка при подключении к базе данных{self.db_path} {e}")
        return connection

    def execute_query(self, query: str):
        """
        Создание и изменение таблиц
        query - команда
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"Произошла ошибка {e}")

    def execute_read_query(self, query: str, as_dict=False):
        """
        Извлекает данные из таблицы
        Принимает SELECT-запрос
        """
        if as_dict:
            self.connection.row_factory = sq.Row
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return (i for i in cursor)
        except Error as e:
            print(f"Произошла ошибка {e}")



def insert_arenda(args):
    """Вставляет данные в бд"""
    insert_command = """
                    INSERT INTO arenda (id_card, title, price, etaj, square, zone, address, description,
                    url, publish_date, parsing_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?);
                        """
    with sq.connect("arenda_bd.db") as db:
        cursor = db.cursor()
        args.append(datetime.now())
        cursor.execute(insert_command, args)
        db.commit()


def check_arenda(id_card):
    """Проверка наличия объявления в БД"""

    with sq.connect("arenda_bd.db") as db:
        select_command = f"""SELECT id_card 
                            FROM arenda 
                            WHERE id_card = {id_card} """
        cursor = db.cursor()
        cursor.execute(select_command)
        result = cursor.fetchall()
        if len(result) == 0:
            return 0
        else:
            return 1


def get_data_from_db():
    """Получение данных из БД"""
    with sq.connect("arenda_bd.db") as db:
        cursor = db.cursor()
        cursor.execute("""SELECT id_card, title, price, etaj, square, zone, address, description,/
                        url, publish_date, parsing_date 
                        FROM arenda""")
        data_set = cursor.fetchall()
        return data_set