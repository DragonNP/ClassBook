import logging
import psycopg2
from psycopg2 import Error


class Database:
    logger = logging.getLogger('database')

    def __init__(self, login, password, database_name, school_name, host='localhost', port='5432'):
        self.connection = None
        self.school_name = None
        self.database_name = database_name
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.school_name = school_name

        self.create_database()
        self.connect()
        self.create_school()

    def create_database(self):
        logger = self.logger
        database = self.database_name
        login = self.login
        password = self.password
        host = self.host
        port = self.port

        connection = psycopg2.connect(user=login,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        connection.autocommit = True

        cursor = connection.cursor()
        cursor.execute("SELECT datname FROM pg_database")
        list_database = [db_name[0] for db_name in cursor.fetchall()]

        if database in list_database:
            logger.debug(f'База данных \'{database}\' уже существует')
            return

        cursor = connection.cursor()
        cursor.execute(f'CREATE DATABASE \'{database}\'')
        cursor.close()
        connection.close()

        logger.info(f'База данных \'{database}\' создана')

    def connect(self):
        logger = self.logger
        database = self.database_name
        login = self.login
        password = self.password
        host = self.host
        port = self.port

        try:
            logger.debug(f'Попытка подключиться к базе данных \'{database}\'')
            # Подключение к существующей базе данных
            connection = psycopg2.connect(user=login,
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)
            connection.autocommit = True
            self.connection = connection

            logger.info(f'База данных \'{database}\' успешно подключена')
        except (Exception, Error) as error:
            logger.error(f'Ошибка при работе с сервером', exc_info=error)

    def close(self):
        self.connection.close()
        self.logger.info('Работа с базой данных завершена')

    def create_school(self):
        logger = self.logger
        connection = self.connection
        school_name = self.school_name

        cursor = connection.cursor()
        try:
            logger.debug(f'Создание таблицы \'{school_name}\'')
            create_table_query = f'''CREATE TABLE IF NOT EXISTS {school_name}
                                  (ID SERIAL NOT NULL,
                                  ФИО TEXT PRIMARY KEY NOT NULL,
                                  Класс TEXT NOT NULL); '''
            cursor.execute(create_table_query)

            logger.debug(f'Таблица \'{school_name}\' создана или уже была создана')
        except (Exception, Error) as error:
            logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
        finally:
            cursor.close()

    def add_student(self, full_name, class_name):
        logger = self.logger
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()
        try:
            check_student = f'select exists (select true from {school} where ФИО=\'{full_name}\')'
            cursor.execute(check_student, (full_name, class_name))

            if cursor.fetchall()[0][0]:
                logger.info(f'Ученик \'{full_name}\' уже был добавлен')
                return

            add_student = f'INSERT INTO {school} (ФИО, Класс) VALUES (%s,%s) RETURNING id'
            cursor.execute(add_student, (full_name, class_name))

            student_id = cursor.fetchone()[0]

            create_person_table = f'''CREATE TABLE IF NOT EXISTS {school}_У{student_id}
                                  (ID date PRIMARY KEY NOT NULL,
                                  Русский int,
                                  Алгебра int,
                                  Геометрия int,
                                  Физика int,
                                  Информатика int); '''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_person_table)

            logger.info("Ученик успешно добавлен")

        except (Exception, Error) as error:
            logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
        finally:
            cursor.close()

    def remove_student(self, full_name, class_name):
        logger = self.logger
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()
        try:
            get_student = f'SELECT * FROM {school} WHERE ФИО=\'{full_name}\' LIMIT 1'
            cursor.execute(get_student, (full_name, class_name))

            student_id = cursor.fetchall()[0][0]

            remove_student = f'''DELETE FROM {school} WHERE id={student_id};
                             DROP TABLE {school}_У{student_id}'''
            cursor.execute(remove_student)

            logger.info(f"Ученик \'{full_name}\' успешно удалён")
        except (Exception, Error) as error:
            logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
        finally:
            cursor.close()
