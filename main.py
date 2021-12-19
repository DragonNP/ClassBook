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


def enter_date():
    while True:
        print(f'Введите дату: (1-{words.back()})', end=' ')
        date = input()

        if date == '1':
            return date
        res = helper.check_date(date)
        if res != '':
            if res == 'OutOfRange':
                print('День находится вне диапазона в месяца')
            else:
                print(words.incorrect_date())
            print()
            continue
        return date


def enter_subject(db: ClassBook, full_name: str):
    while True:
        all_subjects = db.get_subjects(full_name)
        print('Введите предмет:')
        print(helper.format_subjects(all_subjects, words.back()))
        subject = input().lower()

        res = False
        for i in range(len(all_subjects)):
            if subject == all_subjects[i].lower():
                subject = all_subjects[i]
                res = True
                break

        if subject == '1':
            return subject
        if not (res):
            print(words.incorrect_input())
            continue
        return subject


def enter_mark():
    while True:
        print(f'Введите оценку: (1-5 - оценка, 6-{words.back()})', end=' ')
        mark = input()

        if not helper.is_mark(mark):
            print(words.incorrect_input())
            print()
            continue
        return int(mark)


def enter_fullname(db: ClassBook, inverse=False):
    while True:
        print(words.enter_full_name(), end=' ')
        fullname = input()

        if fullname == '1':
            return fullname

        if inverse:
            if db.check_student_exists(fullname):
                print(words.student_already_added())
                continue
        else:
            if not db.check_student_exists(fullname):
                print(words.student_not_found())
                continue
        return fullname


def enter_class():
    while True:
        print(words.enter_class().format(subjects.get_classes()), end=' ')
        class_name = input()

        if class_name == '1':
            return class_name

        if not subjects.check(class_name):
            print(words.incorrect_input())
            print()
            continue
        return class_name


def edit_marks(db: ClassBook, full_name: str):
    while True:
        print(f'\n{words.select_action()}')
        print(tabulate([['1-Добавить или изменить оценку', '4-Оценка по предмету в конкретный день'],
                        ['2-Оценки за день', f'5-{words.back()}'],
                        ['3-Оценки по определённому предмету']]))

        choice = input()

        if (not choice.isdigit()) or int(choice) > 5 or len(choice) != 1:
            print(words.incorrect_input())
            print()
            continue
        else:
            choice = int(choice)

        if choice == 1:
            while True:
                date = enter_date()
                if date == '1':
                    break

                subject = enter_subject(db, full_name)
                if subject == '1':
                    break

                mark = enter_mark()
                if mark == 6:
                    break

                db.add_student_mark(full_name, date, subject, mark)
                print('Оценка успешно добавлена!')
                break

        if choice == 2:
            while True:
                date = enter_date()
                if date == '1':
                    break

                all_marks = db.get_all_marks_by_date(full_name, date)
                result = ''

                if len(all_marks) == 0:
                    result = 'Оценки за этот день не найдены'
                    print(result)
                    break

                for key in all_marks.keys():
                    result += f'{key}: {all_marks[key]}\n'

                print(result)
                break

        if choice == 3:
            while True:
                subject = enter_subject(db, full_name)
                if subject == '1':
                    break

                all_marks = db.get_all_marks(full_name, subject)
                print(helper.format_date_subject(all_marks))
                break

        if choice == 4:
            while True:
                date = enter_date()
                if date == '1':
                    break

                subject = enter_subject(db, full_name)
                if subject == '1':
                    break

                result = db.get_mark_subject_by_date(full_name, subject, date)
                print(result[0][0])
                break

        if choice == 5:
            return


def edit_student(db: ClassBook):
    while True:
        print(f'\n{words.select_action()}')
        print(tabulate(words.student_menu()))

        choice = input()

        if (not choice.isdigit()) or int(choice) > 4 or len(choice) != 1:
            print(words.incorrect_input())
            print()
            continue
        else:
            choice = int(choice)

        if choice == 1:
            while True:
                fullname = enter_fullname(db, inverse=True)
                if fullname == '1':
                    break

                class_name = enter_class()
                if class_name == '1':
                    break

                db.add_student(fullname, class_name)
                print(words.student_added())
                break

        if choice == 2:
            while True:
                fullname = enter_fullname(db)
                if fullname == '1':
                    break

                edit_marks(db, fullname)
                break

        if choice == 3:
            while True:
                print(words.student_confirm(), end=' ')
                choice_rm = input()
                if choice_rm.lower() != words.yes().lower():
                    break

                fullname = enter_fullname(db, inverse=True)
                if fullname == '1':
                    break

                db.remove_student(fullname)
                print(words.student_removed())
                break

        if choice == 4:
            return


def run_school(school: str):
    db = ClassBook(login=loginDB, password=passwordDB, school_name=school,
                   host=hostDB, port=portDB, url=urlDB, useURL=useURL)

    print(f'\n{words.school()}', end='')

    while True:
        print(f'\n{words.select_action()}')
        print(tabulate(words.school_menu()))

        choice = input()

        if (not choice.isdigit()) or int(choice) > 3 or len(choice) != 1:
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


def sel_language():
    while True:
        print(f'Please, enter language ({phrases.get_langs()}):', end=' ')
        lang = input().lower().replace(' ', '')

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
