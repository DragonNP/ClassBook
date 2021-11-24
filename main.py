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


if __name__ == '__main__':
    coloredlogs.install(level='DEBUG')
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)

    load_environment_variables()

    school_name = 'Кантауровская'
    db = Database(loginDB, passwordDB, database_name, school_name)

    full_name = 'Погудалов Никита Валерьевич'
    class_name = '10А физ. мат.'
    db.add_student(full_name, class_name)
    db.add_student_mark(full_name, '24.11.21', 'Русский', 5)
    #db.remove_student(full_name)
    #db.remove_school()
    db.close()
