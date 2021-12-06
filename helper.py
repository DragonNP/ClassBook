import datetime
import logging
from tabulate import tabulate

logger = logging.getLogger('helper')


def is_school_name(name: str):
    if name.isdigit() or len(name) < 5:
        return False
    return True


def check_date(date):
    format = '%d.%m.%y'

    try:
        datetime.datetime.strptime(date, format)
        return True
    except ValueError:
        logger.debug(f'Не правильный формат даты, нужен: {format}')
        return False


def format_date_subject(all_marks):
    result = ''
    format = '%d.%m.%y'

    print(all_marks)
    for mark in all_marks:
        result += f'{mark[0].strftime(format)}: {mark[1]}\n'
    return result


def format_subjects(all_subjects, back_phrase):
    column = 0
    arr = [[], [], []]
    for subject in all_subjects:
        arr[column].append(subject)

        if column == 0:
            column = 1
        elif column == 1:
            column = 2
        elif column == 2:
            column = 0
    arr[2].append(f'1-{back_phrase}')
    return tabulate(arr)
