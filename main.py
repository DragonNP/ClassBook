import logging
import sys
import helper
import phrases
import subjects
from tabulate import tabulate
from classbook import ClassBook

loginDB = None
passwordDB = None
hostDB = None
portDB = None
database_name = 'class_book'
words = None
logger = logging.getLogger('main')
useURL = False
urlDB = None


def basic_config():
    global loginDB, passwordDB, hostDB, portDB, useURL, urlDB

    logging.basicConfig(filename='logs.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    for argument in sys.argv:
        if 'URL_DB' in argument:
            useURL = True
            urlDB = argument.replace('URL_DB=', '')
        if 'LOGIN_DB' in argument:
            loginDB = argument.replace('LOGIN_DB=', '')
        if 'PASSWORD_DB' in argument:
            passwordDB = argument.replace('PASSWORD_DB=', '')
        if 'HOST_DB' in argument:
            hostDB = argument.replace('HOST_DB=', '')
        if 'PORT_DB' in argument:
            portDB = argument.replace('PORT_DB=', '')
        if 'LEVEL' in argument:
            level = logging.getLevelName(argument.replace('LEVEL=', ''))
            logging.getLogger().setLevel(level)

    str_vars = f'URL_DB={urlDB}, LOGIN_DB={loginDB}' \
               f', PASSWORD_DB={passwordDB}, HOST_DB={hostDB}, PORT_DB={portDB}, LEVEL={logging.getLogger().level}'

    if (urlDB is None) and (loginDB is None or passwordDB is None or hostDB is None or portDB is None):
        logger.error(f'Переменные не установлены: {str_vars}')
        return None

    logger.debug(f'Переменные установлены: {str_vars}')
    return True


def edit_marks(db: ClassBook, full_name: str):
    while True:
        print(f'\n{words.select_action()}')
        print(tabulate([['1-Добавить или изменить оценку', '4-Оценка по предмету в конкретный день'],
                        ['2-Оценки за день', f'5-{words.back()}'],
                        ['3-Оценки по определённому предмету']]))
        try:
            choice = input()

            if (not choice.isdigit()) or int(choice) > 5:
                print(words.incorrect_input())
                print()
                continue
            else:
                choice = int(choice)

            if choice == 1:
                while True:
                    print(f'Введите дату: (1-{words.back()})', end=' ')
                    date = input()

                    if date == '1':
                        break
                    if not helper.check_date(date):
                        print(words.incorrect_date())
                        print()
                        continue

                    all_subjects = db.get_subjects(full_name)
                    print('Введите предмет:')
                    print(helper.format_subjects(all_subjects, words.back()))
                    subject = input()

                    if subject == '1':
                        break
                    if not (subject in all_subjects):
                        print(words.incorrect_input())
                        continue

                    print(f'Введите оценку: (1-5 - оценка, 6-{words.back()})', end=' ')
                    mark = input()

                    if not mark.isdigit() or len(mark) != 1 or not (mark in ['1', '2', '3', '4', '5', '6']):
                        print(words.incorrect_input())
                        print()
                        continue
                    else:
                        mark = int(mark)

                    if mark == '6':
                        break

                    db.add_student_mark(full_name, date, subject, mark)
                    print('Оценка успешно добавлена!')
                    break

            if choice == 2:
                while True:
                    print(f'Введите дату: (1-{words.back()})', end=' ')
                    date = input()

                    if date == '1':
                        break
                    if not helper.check_date(date):
                        print(words.incorrect_date())
                        print()
                        continue

                    all_marks = db.get_all_marks_by_date(full_name, date)
                    result = ''

                    for key in all_marks.keys():
                        result += f'{key}: {all_marks[key]}\n'

                    print(result)
                    break

            if choice == 3:
                while True:
                    all_subjects = db.get_subjects(full_name)
                    print('Введите предмет:')
                    print(helper.format_subjects(all_subjects, words.back()))
                    subject = input()

                    if subject == '1':
                        break
                    if not (subject in all_subjects):
                        print(words.incorrect_input())
                        print('!')
                        continue

                    all_marks = db.get_all_marks(full_name, subject)
                    print(helper.format_date_subject(all_marks))
                    break

            if choice == 4:
                while True:
                    all_subjects = db.get_subjects(full_name)
                    print('Введите предмет:')
                    print(helper.format_subjects(all_subjects, words.back()))
                    subject = input()

                    if subject == '1':
                        break
                    if not (subject in all_subjects):
                        print(words.incorrect_input())
                        continue

                    print(f'Введите дату: (1-{words.back()})', end=' ')
                    date = input()

                    if date == '1':
                        break
                    if not helper.check_date(date):
                        print(words.incorrect_date())
                        print()
                        continue

                    result = db.get_mark_subject_by_date(full_name, subject, date)
                    print(result[0][0])
                    break

            if choice == 5:
                return
        except ValueError:
            print(words.incorrect_input(), end=' ')


def edit_student(db: ClassBook):
    while True:
        print(f'\n{words.select_action()}')
        print(tabulate(words.student_menu()))
        try:
            choice = input()

            if (not choice.isdigit()) or int(choice) > 4:
                print(words.incorrect_input())
                print()
                continue
            else:
                choice = int(choice)

            if choice == 1:
                while True:
                    print(words.enter_full_name(), end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if db.check_student_exists(full_name):
                        print(words.student_already_added())
                        break

                    print(words.enter_class().format(subjects.get_classes()), end=' ')
                    class_name = input()

                    if class_name == '1':
                        break

                    if not subjects.check(class_name):
                        print(words.incorrect_input())
                        print()
                        continue

                    db.add_student(full_name, class_name)
                    print(words.student_added())
                    break

            if choice == 2:
                while True:
                    print(words.enter_full_name(), end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print(words.student_not_found())
                        break

                    edit_marks(db, full_name)
                    break

            if choice == 3:
                while True:
                    print(words.student_confirm(), end=' ')
                    choice_rm = input()

                    if choice_rm.lower() != words.yes().lower():
                        break

                    print(words.enter_full_name(), end=' ')
                    full_name = input()

                    if full_name == '1':
                        break

                    if not db.check_student_exists(full_name):
                        print(words.student_not_found())
                        break

                    db.remove_student(full_name)
                    print(words.student_removed())
                    break

            if choice == 4:
                return
        except ValueError:
            print(words.incorrect_input(), end=' ')


def run_school(school: str):
    db = ClassBook(login=loginDB, password=passwordDB, school_name=school,
                   host=hostDB, port=portDB, url=urlDB, useURL=useURL)

    print(f'\n{words.school()}', end='')

    while True:
        print(f'\n{words.select_action()}')
        print(tabulate(words.school_menu()))
        try:
            choice = input()

            if (not choice.isdigit()) or int(choice) > 3:
                print(words.incorrect_input())
                print()
                continue
            else:
                choice = int(choice)

            if choice == 1:
                edit_student(db)

            if choice == 2:
                print(words.school_confirm().format(school_name), end=' ')
                choice_rm = input()

                if choice_rm.lower() == words.yes().lower():
                    db.remove_school()
                    db.close()
                    print(words.school_deleted())
                    return
                else:
                    print(words.school_not_deleted())

            if choice == 3:
                db.close()
                return
        except ValueError:
            print(words.incorrect_input(), end=' ')


def sel_language():
    while True:
        print(f'Please, enter language ({phrases.get_langs()}):', end=' ')
        lang = input()

        if phrases.is_lang(lang):
            words = phrases.Phrases(lang)
            break
        else:
            print('Incorrect input\n')

    return words


if __name__ == '__main__':
    res = basic_config()
    if res is None:
        sys.exit(0)

    words = sel_language()

    print()
    print(words.start_hello())

    while True:
        print(words.enter_school(), end=' ')
        school_name = input()

        if school_name == '1':
            break
        if not helper.is_school_name(school_name):
            print(words.incorrect_input())
            print()
            continue

        run_school(school_name)
        print('\n')
