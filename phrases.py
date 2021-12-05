import logging

langs = ['ru', 'en']


def get_langs():
    return ', '.join(langs)


def is_lang(lang):
    return lang in langs


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
            return 'Enter the school you want to work with (1-Finish the job):'
        elif self.lang == 'ru':
            return 'Введите школу, с которой вы хотите работать (1-Завершить работу):'

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

    def incorrect_date(self):
        if self.lang == 'en':
            return 'Invalid date string format. Must be DD.MM.YY'
        elif self.lang == 'ru':
            return 'Неверный формат строки даты. Должно быть ДД.ММ.ГГ'

    def school(self):
        if self.lang == 'en':
            return 'Great, you\'ve chosen a school'
        elif self.lang == 'ru':
            return 'Отлично, Вы выбрали школу'

    def school_menu(self):
        if self.lang == 'en':
            return [['1-Add/Edit a student', f'3-{self.back()}'], ['2-Delete a school']]
        elif self.lang == 'ru':
            return [['1-Добавить/Редактировать ученика', f'3-{self.back()}'], ['2-Удалить школу']]

    def school_confirm(self):
        if self.lang == 'en':
            return 'Are you sure? Do you really want to delete the school \'{}\'?' + f' ({self.yes()}/No):'
        elif self.lang == 'ru':
            return 'Вы уверены? Вы действительно хотите удалить школу \'{}\'?' + f' ({self.yes()}/Нет):'

    def school_deleted(self):
        if self.lang == 'en':
            return 'School removed'
        elif self.lang == 'ru':
            return 'Школа удалена'

    def school_not_deleted(self):
        if self.lang == 'en':
            return 'The school has not been deleted'
        elif self.lang == 'ru':
            return 'Школа не была удалена'

    def student_menu(self):
        if self.lang == 'en':
            return [['1-Add a student', f'3-Delete a student'], ['2-Add/Change mark', f'4-{self.back()}']]
        elif self.lang == 'ru':
            return [['1-Добавить ученика', '3-Удалить ученика'], ['2-Добавить/Изменить оценку', f'4-{self.back()}']]

    def enter_full_name(self):
        if self.lang == 'en':
            return f'Enter the student\'s full name (1-{self.back()}):'
        elif self.lang == 'ru':
            return f'Введите ФИО ученика (1-{self.back()}):'

    def student_already_added(self):
        if self.lang == 'en':
            return 'The student has already been added'
        elif self.lang == 'ru':
            return 'Ученик уже был добавлен'

    def enter_class(self):
        if self.lang == 'en':
            return 'Enter the class in which the student is studying ({})'
        elif self.lang == 'ru':
            return 'Введите класс, в котором обучается ученик ({})' + f' (1-{self.back()}):'

    def student_added(self):
        if self.lang == 'en':
            return 'Student added'
        elif self.lang == 'ru':
            return 'Ученик добавлен'

    def student_removed(self):
        if self.lang == 'en':
            return 'Student removed'
        elif self.lang == 'ru':
            return 'Ученик удалён'

    def student_not_found(self):
        if self.lang == 'en':
            return 'The student does not exist'
        elif self.lang == 'ru':
            return 'Ученика не существует'

    def student_confirm(self):
        if self.lang == 'en':
            return f'Are you sure? Do you really want to delete a student? ({self.yes()}/No):'
        elif self.lang == 'ru':
            return f'Вы уверены? Вы действительно хотите удалить ученика? ({self.yes()}/Нет):'

    def yes(self):
        if self.lang == 'en':
            return 'Yes'
        elif self.lang == 'ru':
            return 'Да'

    def back(self):
        if self.lang == 'en':
            return 'Back'
        elif self.lang == 'ru':
            return 'Назад'

