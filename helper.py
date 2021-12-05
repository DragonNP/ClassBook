import datetime
import logging

logger = logging.getLogger('helper')


def is_correct_school_name(name: str):
    if name.isdigit() or len(name) < 5:
        return False
    return True


def check_date(date):
    format = '%d.%m.%y'

    try:
        datetime.datetime.strptime(date, format)
        return True
    except ValueError:
        logger.debug(f'Не правильный формат даты нужен: {format}')
        return False
