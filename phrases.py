import logging


def langs():
    return 'ru, en'


class Phrases:
    logger = logging.getLogger('phrases')

    def __init__(self, lang='en'):
        if lang in ['en', 'ru']:
            self.lang = lang
            return

        self.logger.error(f'Language undefined: \'{lang}\'. Set default: \'en\'')
        self.lang = 'en'

    def start_hello(self):
        if self.lang == 'en':
            return 'Hi! This is a console application, a prototype of an online class book.'
        elif self.lang == 'ru':
            return 'Привет! Это консольное приложение, прототип электронного журнала.'

    def enter_school(self):
        if self.lang == 'en':
            return 'To work, enter the school you want to work with (1-Finish the job):'
        elif self.lang == 'ru':
            return 'Для работы, введите школу, с которой вы хотите работать (1-Завершить работу):'

    def select_action(self):
        if self.lang == 'en':
            return 'Select an action'
        elif self.lang == 'ru':
            return 'Выберите действие'

    def incorrect_data(self):
        if self.lang == 'en':
            return 'Incorrect data entry'
        elif self.lang == 'ru':
            return 'Неправильный ввод данных'
