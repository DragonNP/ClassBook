from psycopg2 import Error
import coloredlogs, logging
from database import Database
import os

loginDB = None
passwordDB = None
hostDB = 'localhost'
portDB = '5432'
database_name = 'class_book'

logger = logging.getLogger('main')


def load_environment_variables():
    global loginDB, passwordDB

    loginDB = os.environ['LOGIN_DB']
    passwordDB = os.environ['PASSWORD_DB']

    if not loginDB or not passwordDB:
        logger.error('Логин и пароль для базы данных не установлен')


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


if __name__ == '__main__':
    coloredlogs.install(level='DEBUG')
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    load_environment_variables()

    school_name = 'Кантауровская'
    db = Database(loginDB, passwordDB, database_name, school_name)

    full_name = 'Погудалов Никита Валерьевич'
    class_name = '10А физ. мат.'
    #db.add_student(full_name, class_name)
    #db.remove_student(full_name)
    db.remove_school()
    db.close()
