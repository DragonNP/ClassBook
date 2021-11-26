import logging
import psycopg2
from psycopg2 import Error

import subjects


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

    def remove_school(self):
        logger = self.logger
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()
        try:
            get_students = f'SELECT * FROM {school}'
            cursor.execute(get_students)

            for student in cursor.fetchall():
                self.remove_student(student[1])

            remove_school = f'DROP TABLE {school}'
            cursor.execute(remove_school)

            logger.info(f'Школа \'{school}\' успешно удалена')
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
            if subjects.get(class_name) is None:
                logger.info('Формат класса не верный')
                return

            check_student = f'select exists (select true from {school} where ФИО=\'{full_name}\')'
            cursor.execute(check_student, (full_name, class_name))

            if cursor.fetchall()[0][0]:
                logger.info(f'Ученик \'{full_name}\' уже был добавлен')
                return

            add_student = f'INSERT INTO {school} (ФИО, Класс) VALUES (%s,%s) RETURNING id'
            cursor.execute(add_student, (full_name, class_name))

            student_id = cursor.fetchone()[0]

            create_person_table = f'''CREATE TABLE IF NOT EXISTS {school}_У{student_id}
                                  (ID date PRIMARY KEY NOT NULL, {subjects.get(class_name)}); '''
            # Выполнение команды: это создает новую таблицу
            cursor.execute(create_person_table)

            logger.info(f'Ученик \'{full_name}\' успешно добавлен')

        except (Exception, Error) as error:
            logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
        finally:
            cursor.close()

    def remove_student(self, full_name):
        logger = self.logger
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()
        try:
            get_student = f'SELECT * FROM {school} WHERE ФИО=\'{full_name}\' LIMIT 1'
            cursor.execute(get_student)

            student_id = cursor.fetchall()[0][0]

            remove_student = f'''DELETE FROM {school} WHERE id={student_id};
                             DROP TABLE {school}_У{student_id}'''
            cursor.execute(remove_student)

            logger.info(f"Ученик \'{full_name}\' успешно удалён")
        except (Exception, Error) as error:
            logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
        finally:
            cursor.close()

    def add_student_mark(self, full_name, date_mark, subject, mark):
        logger = self.logger
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()
        try:
            logger.debug(f'Добавление оценки \'{full_name}\' {date_mark} {subject} {mark}')

            get_student = f'SELECT * FROM {school} WHERE ФИО=\'{full_name}\' LIMIT 1'
            cursor.execute(get_student)

            student_id = cursor.fetchall()[0][0]

            cursor.execute(f'select exists(select 1 from {school}_У{student_id} where id=\'{date_mark}\')')

            if cursor.fetchone()[0]:
                add_mark = f'UPDATE {school}_У{student_id} SET {subject} = \'{mark}\' WHERE id = \'{date_mark}\''
            else:
                add_mark = f'INSERT INTO {school}_У{student_id} (id, {subject}) VALUES (\'{date_mark}\',{mark})'
            cursor.execute(add_mark)

            logger.debug(f'Оценка успешно добавлена \'{full_name}\' {date_mark} {subject} {mark}')
        except (Exception, Error) as error:
            logger.error("Ошибка при работе с PostgreSQL", exc_info=error)
        finally:
            cursor.close()

    def get_subjects(self, full_name):
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()

        get_student = f'SELECT * FROM {school} WHERE ФИО=\'{full_name}\' LIMIT 1'
        cursor.execute(get_student)

        student_id = cursor.fetchall()[0][0]

        return self.get_subjects_by_id(student_id)

    def get_subjects_by_id(self, student_id):
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()

        get_subjects_request = f'SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name=\'{school}_У{student_id}\''
        cursor.execute(get_subjects_request)
        return [i[0] for i in cursor.fetchall() if i[0] != 'id']

    def get_all_marks(self, full_name, subject):
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()

        get_student = f'SELECT * FROM {school} WHERE ФИО=\'{full_name}\' LIMIT 1'
        cursor.execute(get_student)

        student_id = cursor.fetchall()[0][0]

        get_subjects_request = f'SELECT id, {subject} FROM {school}_У{student_id} GROUP BY id'
        cursor.execute(get_subjects_request)
        return [i for i in cursor.fetchall()]

    def get_mark_subject_by_date(self, full_name, subject, date):
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()

        get_student = f'SELECT * FROM {school} WHERE ФИО=\'{full_name}\' LIMIT 1'
        cursor.execute(get_student)

        student_id = cursor.fetchall()[0][0]

        get_subjects_request = f'SELECT {subject} FROM {school}_У{student_id} WHERE id=\'{date}\''
        cursor.execute(get_subjects_request)
        return [i for i in cursor.fetchall()]

    def get_all_marks_by_date(self, full_name, date):
        connection = self.connection
        school = self.school_name

        cursor = connection.cursor()

        get_student = f'SELECT * FROM {school} WHERE ФИО=\'{full_name}\' LIMIT 1'
        cursor.execute(get_student)

        student_id = cursor.fetchall()[0][0]

        get_subjects_request = f'SELECT * FROM {school}_У{student_id} WHERE id=\'{date}\''
        cursor.execute(get_subjects_request)

        subjects = self.get_subjects_by_id(student_id)
        row = [i for i in cursor.fetchall()][0]
        result = {}

        for i in range(1, len(row)):
            if row[i] is None:
                continue
            result[subjects[i-1]] = row[i]

        return result
