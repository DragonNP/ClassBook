import datetime
import logging
from tabulate import tabulate

logger = logging.getLogger('helper')


def is_school_name(name: str):
    if name.isdigit() or len(name) < 5 or name[0] == ' ':
        return False
    return True


def check_date(date):
    format = '%d.%m.%y'

    try:
        datetime.datetime.strptime(date, format)
        return ''
    except ValueError as e:
        logger.debug(f'Не правильный формат даты, нужен: {format}')
        if str(e) == 'day is out of range for month':
            return 'OutOfRange'
        return 'ValueError'


def format_date_subject(all_marks):
    result = ''
    format = '%d.%m.%y'

    for mark in all_marks:
        if mark[1] is None:
            continue

        date = mark[0].strftime(format)
        result += f'{date}: {mark[1]}\n'
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


def is_mark(mark: str):
    return not(not mark.isdigit() or len(mark) != 1 or not (mark in ['1', '2', '3', '4', '5', '6']))
