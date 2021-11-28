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
                        ['2-Все оценки за день', f'5-{phrase.back()}'],
                        ['3-Все оценки по определённому предмету']]))
        try:
            choice = int(input())

            if choice == 1:
                while True:
                    print(f'Введите дату: (1-{phrase.back()})', end=' ')
                    date = input()

                    if date == '1':
                        break

                    all_subjects = db.get_subjects(full_name)
                    print(f'Введите предмет:\n{all_subjects}, 1-{phrase.back()}', end=' ')
                    subject = input()

                    if subject == '1':
                        break
                    if not(subject in all_subjects):
                        print(phrase.incorrect_data())
                        continue

                    print(f'Введите оценку: (1-5 - оценка, 6-{phrase.back()}', end=' ')
                    try:
                        mark = int(input())
                    except ValueError:
                        print(phrase.incorrect_data(), end=' ')
                        continue
                    if mark == '6':
                        break

                    db.add_student_mark(full_name, date, subject, mark)
                    print('Оценка успешно добавлена!')
                    break

            if choice == 2:
                while True:
                    print(f'Введите дату: (1-{phrase.back()})', end=' ')
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
                    print(f'Введите предмет:\n{all_subjects}, 1-{phrase.back()}', end=' ')
                    subject = input()

                    if subject == '1':
                        break
                    if not(subject in all_subjects):
                        print(phrase.incorrect_data())
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
                    print(f'Введите предмет:\n{all_subjects}, 1-{phrase.back()}', end=' ')
                    subject = input()

                    if subject == '1':
                        break
                    if not(subject in all_subjects):
                        print(phrase.incorrect_data())
                        continue

                    print(f'Введите дату: (1-{phrase.back()})', end=' ')
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
        print(tabulate(phrase.student_menu()))
        try:
            choice = int(input())

            if choice == 1:
                while True:
                    print(phrase.enter_full_name(), end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if db.check_student_exists(full_name):
                        print(phrase.student_already_added())
                        break

                    print(phrase.enter_class().format(subjects.get_classes()), end=' ')
                    class_name = input()

                    if class_name == '1':
                        break

                    if not subjects.check(class_name):
                        print(phrase.incorrect_data(), end=' ')
                        continue

                    db.add_student(full_name, class_name)
                    print(phrase.student_added())
                    break

            if choice == 2:
                while True:
                    print(phrase.enter_full_name(), end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print(phrase.student_not_found())
                        break

                    edit_marks(db, full_name)
                    break

            if choice == 3:
                while True:
                    print(phrase.student_confirm(), end=' ')
                    choice_rm = input()

                    if choice_rm != phrase.yes():
                        break

                    print(phrase.enter_full_name(), end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print(phrase.student_not_found())
                        break

                    db.remove_student(full_name)
                    print(phrase.student_removed())
                    break

            if choice == 4:
                return
        except ValueError:
            print(phrase.incorrect_data(), end=' ')


def run_school(school):
    db = Database(loginDB, passwordDB, database_name, school)

    print(f'\n{phrase.school()}', end='')

    while True:
        print(f'\n{phrase.select_action()}')
        print(tabulate(phrase.school_menu()))
        try:
            choice = int(input())

            if choice == 1:
                edit_student(db)

            if choice == 2:
                print(phrase.school_confirm().format(school_name), end=' ')
                choice_rm = input()

                if choice_rm == phrase.yes():
                    db.remove_school()
                    db.close()
                    print(phrase.school_deleted())
                    return
                else:
                    print(phrase.school_not_deleted())

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
