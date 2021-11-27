import coloredlogs
import logging

import subjects
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


def edit_marks(db: Database, full_name):
    print()
    while True:
        print('\nВыберите действие (1-Добавить/Изменить оценку, 2-Получить все оценки по опр. предмету, '
              '3-Получить оценки по предмету в опр. день, 4-Получить все оценки за день, 5-Назад:', end=' ')
        try:
            choice = int(input())

            if choice == 1:
                while True:
                    print('Введите дату: (1-Назад)', end=' ')
                    date = input()

                    if date == '1':
                        break

                    all_subjects = db.get_subjects(full_name)
                    print(f'Введите предмет:\n{all_subjects}, 1-Назад', end=' ')
                    subject = input()

                    if subject == '1':
                        break
                    if not(subject in all_subjects):
                        print('Введен не правильный предмет')
                        continue

                    print(f'Введите оценку: (1-5 - оценка, 6-Назад', end=' ')
                    try:
                        mark = int(input())
                    except ValueError:
                        print('Не правильный ввод данных.', end=' ')
                        continue
                    if mark == '6':
                        break

                    db.add_student_mark(full_name, date, subject, mark)
                    print('Оценка успешно добавлена!')
                    break

            if choice == 2:
                while True:
                    all_subjects = db.get_subjects(full_name)
                    print(f'Введите предмет:\n{all_subjects}, 1-Назад', end=' ')
                    subject = input()

                    if subject == '1':
                        break
                    if not(subject in all_subjects):
                        print('Введен не правильный предмет')
                        continue

                    all_marks = db.get_all_marks(full_name, subject)
                    result = ''
                    for mark in all_marks:
                        result += f'{mark[0]}: {mark[1]}\n'
                    print(result)
                    break

            if choice == 3:
                while True:
                    all_subjects = db.get_subjects(full_name)
                    print(f'Введите предмет:\n{all_subjects}, 1-Назад', end=' ')
                    subject = input()

                    if subject == '1':
                        break
                    if not(subject in all_subjects):
                        print('Введен не правильный предмет')
                        continue

                    print('Введите дату: (1-Назад)', end=' ')
                    date = input()

                    if date == '1':
                        break

                    result = db.get_mark_subject_by_date(full_name, subject, date)
                    print(result[0][0])
                    break

            if choice == 4:
                while True:
                    print('Введите дату: (1-Назад)', end=' ')
                    date = input()

                    if date == '1':
                        break

                    all_marks = db.get_all_marks_by_date(full_name, date)
                    result = ''

                    for key in all_marks.keys():
                        result += f'{key}: {all_marks[key]}\n'

                    print(result)
                    break

            if choice == 5:
                return
        except ValueError:
            print('Не правильный ввод данных.', end=' ')


def edit_student(db: Database):
    print('\n')
    while True:
        print('Выберите действие (1-Добавить ученика, 2-Удалить ученика, 3-Добавить/Изменить оценку, 4-Назад):',
              end=' ')
        try:
            choice = int(input())

            if choice == 1:
                is_Break = False
                while not is_Break:
                    print('Введите ФИО ученика, которого надо добавить: (1-Назад)', end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if db.check_student_exists(full_name):
                        print('Ученик уже был добавлен.')
                        continue

                    print(f'Введите класс, в котором обучается ученик ({subjects.get_classes()}): (1-Назад)', end=' ')
                    class_name = input()

                    if class_name == '1':
                        break

                    if not subjects.check(class_name):
                        print('Не правильный тип класса.', end=' ')
                        continue

                    db.add_student(full_name, class_name)
                    print('Отлично, ученик добавлен!')
                    break

            if choice == 2:
                while True:
                    print(f'Вы уверены? Вы действительно хотите удалить ученика? (Да/Нет):', end=' ')
                    choice_rm = input()

                    if choice_rm != 'Да':
                        break

                    print('Введите ФИО ученика, которого надо удалить: (1-Назад)', end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print('Ученика не существует.')
                        continue

                    db.remove_student(full_name)
                    print('Ученик успешно удалён!')
                    break

            if choice == 3:
                while True:
                    print('Введите ФИО ученика, которого надо удалить: (1-Назад)', end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print('Ученика не существует.')
                        continue

                    edit_marks(db, full_name)
                    break

            if choice == 4:
                return
        except ValueError:
            print('Не правильный ввод данных.', end=' ')


def run_school(school):
    db = Database(loginDB, passwordDB, database_name, school)

    print(f'\nОтлично, Вы выбрали школу.')

    while True:
        print('Выберите что вы хотите сделать? (1-Удалить школу, 2-Добавить/Редактировать ученика, 3-Назад):', end=' ')
        try:
            choice = int(input())

            if choice == 1:
                print(f'Вы уверены? Вы действительно ходите удалить школу \'{school}\'? (Да/Нет):', end=' ')
                choice_rm = input()

                if choice_rm == 'Да':
                    db.remove_school()
                    db.close()
                    print('Школа успешно удалена\nВозврат к началу...')
                    return
                else:
                    print('Школа не была удалена.')
            if choice == 2:
                edit_student(db)
            if choice == 3:
                db.close()
                return
        except ValueError:
            print('Не правильный ввод данных.', end=' ')


if __name__ == '__main__':
    coloredlogs.install(level='INFO')
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    load_environment_variables()

    print('Привет! Это консольное приложие, прототип электроного журнала.')
    while True:
        print('Для работы напишите школу, с которой вы хотите работать:', end=' ')
        school_name = input()

        run_school(school_name)

    #db.add_student_mark(full_name, '24.11.21', 'Алгебра', 5)
    #db.add_student(full_name, class_name)
    #print(db.get_subjects(full_name))
    #db.remove_student(full_name)
    #db.remove_school()
    #db.close()

