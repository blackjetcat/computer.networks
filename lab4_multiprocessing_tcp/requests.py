"""
Модуль для формирования запросов
для отправки на сервер
"""


import pickle


# Класс с информацией о персонале
class Student:
    def __init__(self, surname, maths, physics, birth):
        self.surname = surname
        self.maths = maths
        self.physics = physics
        self.birth = birth

    def printw(self):
        print('   surname: ', self.surname)
        print('  maths: ', self.maths)
        print('    physics: ', self.physics)
        print('birth date: ', self.birth)


def print_data(data):
    print('-------------------')
    for i in range(len(data)):
        data[i].printw()
        print('-------------------')


# Формирования запроса на просмотра данных
def print_request():
    request = ('print',)
    request = pickle.dumps(request)
    return request


# Формирвоания запроса на добавление элемента
def add_request():
    surname = input('enter surname: ')
    maths = input('enter maths grade: ')
    physics = input('enter physics grade: ')
    birth = input('enter birth date: ')
    tmp = Student(surname, maths, physics, birth)
    request = ('add', tmp)
    request = pickle.dumps(request)
    return request


# Формирование запроса для редактирвоание записи
def edit_request():
    n = input('enter element to edit: ')
    print('1. - rewrite note\n2. - edit note field')
    switch = input('input> ')
    # Выбираем, редактировать поле
    # Или же полностью перезаписать элемент
    if switch == '1':
        # Формируем запроса на перезаписывание элемента
        surname = input('enter new surname: ')
        maths = input('enter new maths grade: ')
        physics = input('enter new physics grade: ')
        birth = input('enter new birth date: ')
        tmp = Student(surname, maths, physics, birth)
        request = ('edit', int(n), 'rewrite', tmp)
        return request
    elif switch == '2':
        # Формируем запрос на редактирования поля записи
        print('enter number of field to edit (1, 2, 3,4)')
        print('or enter "/field_name", for example "/surname"')
        f = input('input> ')
        # Выбираем поле для редактирования
        if f == '2' or f == '/surname':
            field = input('enter new surname: ')
            request = ('edit', int(n), 'edit', 'surname', field)
            request = pickle.dumps(request)
            return request
        elif f == '2' or f == '/maths':
            field = input('enter new maths: ')
            request = ('edit', int(n), 'edit', 'maths', field)
            request = pickle.dumps(request)
            return request
        elif f == '3' or f == '/physics':
            field = input('enter new physics: ')
            request = ('edit', int(n), 'edit', 'physics', field)
            request = pickle.dumps(request)
            return request
        elif f == '4' or f == '/birth':
            field = input('enter new birth date: ')
            request = ('edit', int(n), 'edit', 'birth', field)
            request = pickle.dumps(request)
            return request
        else:
            print('input error!')
            return False
    else:
        print('input error!')
        return False


# Формирование запроса на удаление элемента
def delete_request():
    n = input('enter number of element to delete: ')
    request = ('delete', int(n))
    request = pickle.dumps(request)
    return request


# Формирование запроса на сортировку
def sort_request():
    print('enter number of field to sort by (1, 2, 3 ,4)')
    print('or enter "/field_name", for example "/surname"')
    f = input('input> ')
    if f == '1' or f == '/surname':
        request = ('sort', 'surname')
        request = pickle.dumps(request)
        return request
    elif f == '2' or '/maths':
        request = ('sort', 'maths')
        request = pickle.dumps(request)
        return request
    elif f == '3' or '/physics':
        request = ('sort', 'physics')
        request = pickle.dumps(request)
        return request
    elif f == '4' or f == 'birth':
        request = ('sort', 'birth')
        request = pickle.dumps(request)
        return request
    else:
        print('input error!')
        return False
