import coloredlogs
import logging
from tabulate import tabulate

import phrases
import subjects
from database import Database
import os

loginDB = None
passwordDB = None
hostDB = 'localhost'
portDB = '5432'
database_name = 'class_book'
phrase = None
logger = logging.getLogger('main')


def load_environment_variables():
    global loginDB, passwordDB

    loginDB = os.environ['LOGIN_DB']
    passwordDB = os.environ['PASSWORD_DB']

    if not loginDB or not passwordDB:
        logger.error('Логин и пароль для базы данных не установлен')


def edit_marks(db: Database, full_name):
    while True:
        print(f'\n{phrase.select_action()}')
        print(tabulate([['1-Добавить или изменить оценку', '4-Оценки по предмету в конкретный день'],
                        ['2-Все оценки за день', '5-Назад'],
                        ['3-Все оценки по определённому предмету']]))
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

                    all_marks = db.get_all_marks(full_name, subject)
                    result = ''
                    for mark in all_marks:
                        result += f'{mark[0]}: {mark[1]}\n'
                    print(result)
                    break

            if choice == 4:
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

            if choice == 5:
                return
        except ValueError:
            print(phrase.incorrect_data(), end=' ')


def edit_student(db: Database):
    while True:
        print(f'\n{phrase.select_action()}')
        print(tabulate([['1-Добавить ученика', '3-Удалить ученика'],
                        ['2-Добавить/Изменить оценку', '4-Назад']]))
        try:
            choice = int(input())

            if choice == 1:
                while True:
                    print('Введите ФИО ученика (1-Назад):', end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if db.check_student_exists(full_name):
                        print('Ученик уже был добавлен.')
                        break

                    print(f'Введите класс, в котором обучается ученик ({subjects.get_classes()}) (1-Назад):', end=' ')
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
                    print('Введите ФИО ученика (1-Назад):', end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print('Ученика не существует.')
                        continue

                    edit_marks(db, full_name)
                    break

            if choice == 3:
                while True:
                    print(f'Вы уверены? Вы действительно хотите удалить ученика? (Да/Нет):', end=' ')
                    choice_rm = input()

                    if choice_rm != 'Да':
                        break

                    print('Введите ФИО ученика (1-Назад):', end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print('Ученик не найден')
                        break

                    db.remove_student(full_name)
                    print('Ученик успешно удалён!')
                    break

            if choice == 4:
                return
        except ValueError:
            print(phrase.incorrect_data(), end=' ')


def run_school(school):
    db = Database(loginDB, passwordDB, database_name, school)

    print(f'\nОтлично, Вы выбрали школу.', end='')

    while True:
        print(f'\n{phrase.select_action()}')
        print(tabulate([['1-Добавить/Редактировать ученика', '3-Назад'],
                        ['2-Удалить школу']]))
        try:
            choice = int(input())

            if choice == 1:
                edit_student(db)

            if choice == 2:
                print(f'Вы уверены? Вы действительно ходите удалить школу \'{school}\'? (Да/Нет):', end=' ')
                choice_rm = input()

                if choice_rm == 'Да':
                    db.remove_school()
                    db.close()
                    print('Школа успешно удалена\nВозврат к началу...')
                    return
                else:
                    print('Школа не была удалена.')

            if choice == 3:
                db.close()
                return
        except ValueError:
            print(phrase.incorrect_data(), end=' ')


if __name__ == '__main__':
    coloredlogs.install(level='INFO')
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    load_environment_variables()

    print(f'Please, enter language ({phrases.langs()}):', end=' ')
    lang = input()
    phrase = phrases.Phrases(lang)

    print(phrase.start_hello())

    while True:
        print(phrase.enter_school(), end=' ')
        school_name = input()

        if school_name == '1':
            break

        run_school(school_name)
        print('\n')
