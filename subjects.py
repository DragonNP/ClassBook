import re


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
    return f'''{get_10_base()},
"Прикл. мех." int'''


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