import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import logging
import os

loginDB = None
passwordDB = None
hostDB = 'localhost'
portDB = '5432'
school_name = ''

connectionDB = None

logger = logging.getLogger('main')


def load_logging():
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    pass


def load_environment_variables():
    global loginDB, passwordDB

    loginDB = os.environ['LOGIN_DB']
    passwordDB = os.environ['PASSWORD_DB']

    logger.debug('Переменные установлены')


def load_database():
    global connectionDB

    logger.debug('Подключение к PostgreSQL')

    try:
        # Подключение к существующей базе данных
        connectionDB = psycopg2.connect(user=loginDB,
                                        # пароль, который указали при установке PostgreSQL
                                        password=passwordDB,
                                        host=hostDB,
                                        port=portDB,
                                        database='class_book')
        connectionDB.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        logger.debug('Подключение к PostgreSQL успешно')
    except (Exception, Error) as error:
        logger.error("Ошибка при работе с PostgreSQL", exc_info=error)


def create_database():
    logger.debug('Создание базы данных')
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=loginDB,
                                        # пароль, который указали при установке PostgreSQL
                                        password=passwordDB,
                                        host=hostDB,
                                        port=portDB)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        sql_create_database = 'CREATE DATABASE class_book'
        cursor.execute(sql_create_database)

        logger.debug('База данных создана')
    except (Exception, Error) as error:
        logger.error("Ошибка при создании базы данных", exc_info=error)
    finally:
        cursor.close()
        connection.close()


def select_school():
    global connectionDB, school_name
    try:
        logger.info('Введите название школы: ')
        school_name = 'Кантауровская' #input()

        # Создайте курсор для выполнения операций с базой данных
        cursor = connectionDB.cursor()

        # SQL-запрос для создания новой таблицы
        create_table_query = f'''CREATE TABLE IF NOT EXISTS {school_name}
                              (ID SERIAL NOT NULL,
                              ФИО TEXT PRIMARY KEY NOT NULL,
                              Класс TEXT NOT NULL); '''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)

        connectionDB.commit()

        logger.info("Подключение успешно")

    except (Exception, Error) as error:
        logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
    finally:
        cursor.close()


def add_student():
    global connectionDB, school_name
    try:
        logger.info('Введите полное имя ученика:')
        name = 'Погудалов Никита Валерьевич' #input()
        logger.info('Введите класс, в котором обучается ученик:')
        class_ = '10А физ. мат.' #input()

        cursor = connectionDB.cursor()

        add_person = f""" INSERT INTO {school_name} (ФИО, Класс) VALUES (%s,%s) RETURNING id;"""
        cursor.execute(add_person, (name, class_))
        connectionDB.commit()

        student_id = cursor.fetchone()[0]

        create_person_table = f'''CREATE TABLE IF NOT EXISTS {school_name}_У{student_id}
                              (ID date PRIMARY KEY NOT NULL,
                              Русский int,
                              Алгебра int,
                              Геометрия int,
                              Физика int,
                              Информатика int); '''
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_person_table)
        connectionDB.commit()

        logger.info("Ученик успешно добавлен")

    except (Exception, Error) as error:
        logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
    finally:
        cursor.close()


def add_student_mark():
    global connectionDB, school_name
    try:
        logger.info('Введите полное имя ученика:')
        name = 'Погудалов Никита Валерьевич' #input()

        cursor = connectionDB.cursor()

        get_id_by_name = f"""SELECT id FROM {school_name} WHERE ФИО = '{name}' """
        cursor.execute(get_id_by_name)
        connectionDB.commit()

        student_id = cursor.fetchone()[0]

        cursor.execute(f"""SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = '{school_name}_У{student_id}';""")
        connectionDB.commit()

        subjects = ', '.join([i[0] for i in cursor.fetchall() if i[0] != 'id'])

        logger.info(f'Введите предмет, по которому надо поставить оценку {subjects}:')
        subject = 'Русский' #input()
        logger.info('Введите саму оценку:')
        mark = '5' #input()


        logger.info('Введите дату:')
        date = '23.11.2021'

        while True:
            cursor.execute(f"""select exists(select 1 from {school_name}_У{student_id} where id='{date}')""")
            connectionDB.commit()

            if not cursor.fetchone()[0]:
                break
            logger.info('На эту дату уже есть оценки, введите другую:')
            date = input()


        add_mark = f""" INSERT INTO {school_name}_У{student_id} (id, {subject}) VALUES (%s,%s)"""
        cursor.execute(add_mark, (date, mark))
        connectionDB.commit()

        logger.info("Оценка успешно добавлена")

    except (Exception, Error) as error:
        logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
    finally:
        cursor.close()


def test():
    global connectionDB


if __name__ == '__main__':
    load_logging()
    load_environment_variables()
    #create_database()
    load_database()

    select_school()
    #add_student()
    add_student_mark()
    connectionDB.close()
