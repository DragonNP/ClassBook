import re

rus_letters = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П',
                   'Р', 'С', 'Т','У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я']
classes = ['10{} физ. мат.', '10{} база', '9{}']


def get_classes():
    return ', '.join(name.format('(Буква)') for name in classes)


def check(class_name: str):
    if len(class_name) > 3:
        letter = class_name[2]
    elif len(class_name) == 2:
        letter = class_name[1]
    else:
        return False

    if not letter.upper() in rus_letters:
        return False
    if class_name in [name.format(letter) for name in classes]:
        return True
    return False


def get(class_name):
    if re.match(r"10(?u)\w+ физ. мат.", class_name):
        return get_10_math()
    elif re.match(r"10(?u)\w+ база", class_name):
        return get_10_base()
    elif re.match(r"9(?u)\w+", class_name):
        return get_9()
    else:
        return None


def get_9():
    return f'''{get_def_subjects()}, "Черчение" int'''


def get_10_base():
    return f'''{get_def_subjects()}, "Индивидуальный проект" int'''


def get_10_math():
    return f'''{get_10_base()}, "Прикл. мех." int'''


def get_def_subjects():
    return '''"Алгебра" int,
"Англ. яз." int,
"Биология" int,
"География" int,
"Геометрия" int,
"Информатика" int,
"История" int,
"Литература" int,
"ОБЖ" int,
"Обществознание" int,
"Род.лит.(рус)" int,
"Русский язык" int,
"Физика" int,
"Физкультура" int,
"Химия" int'''