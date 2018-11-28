import socket
import pickle
import os
from multiprocessing import Process


# Класс с иформацией о персонале
class Student:
    def __init__(self, surname, maths, physics, birth):
        self.surname = surname
        self.maths = maths
        self.physics = physics
        self.birth = birth

    def printw(self):
        print('\n   surname: ', self.surname)
        print('  maths: ', self.maths)
        print('    physics: ', self.physics)
        print('birth date: ', self.birth)


# Утилити функции для обозначения ключа сортировки
def by_surname(student):
    return student.surname


def by_maths(student):
    return student.maths


def by_physics(student):
    return student.physics


def by_birth(student):
    return student.birth


notes = []


def sort(r):
    global notes
    if r == 'surname':
        notes = sorted(notes, key=by_surname)
    elif r == 'maths':
        notes = sorted(notes, key=by_maths)
    elif r == 'physics':
        notes = sorted(notes, key=by_physics)
    elif r == 'birth':
        notes = sorted(notes, key=by_birth)
    print('notes sorted by ', r)


# Процесс
def process_task(port):
    print('new process started, pid: ', os.getpid())
    process_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    process_socket.bind(('localhost', port))
    process_socket.listen(1)
    client_conn, address = process_socket.accept()
    print('client ', address, ' redirected to port ', port)
    while True:
        r = client_conn.recv(1024)
        r = pickle.loads(r)
        print('new', r[0], 'request received from ', address)
        # Обработка запроса на добавление
        if r[0] == 'add':
            notes.append(r[1])
            print('new note has been added:')
            r[1].printw()
            message = 'note has been added'
            message = pickle.dumps(message)
            client_conn.send(message)
        # Обработка запроса на просмотр данных
        elif r[0] == 'print':
            resp = pickle.dumps(notes)
            client_conn.send(resp)
            print('data was sent to ', address)
        # Обработка запроса на редактирование данных
        elif r[0] == 'edit':
            i = r[1]
            # Ошибка о попытке обратиться к несуществующему элементу
            if i >= len(notes):
                print('ran out of range')
                message = 'ran out of range'
                message = pickle.dumps(message)
                client_conn.send(message)
                continue
            # Перезаписывание элемента
            if r[2] == 'rewrite':
                notes[i] = r[3]
                print('note has been edited: ')
                notes[i].printw()
                message = 'note has been edited'
                message = pickle.dumps(message)
                client_conn.send(message)
            # Редактирование поля
            elif r[2] == 'edit':
                if r[3] == 'surname':
                    notes[i].surname = r[4]
                elif r[3] == 'maths':
                    notes[i].maths = r[4]
                elif r[3] == 'physics':
                    notes[i].physics = r[4]
                elif r[3] == 'birth':
                    notes[i].birth = r[4]
        # Обработка запроса на удаление
        elif r[0] == 'delete':
            i = r[1]
            if i >= len(notes):
                print('ran out of range')
                message = 'ran out of range'
                message = pickle.dumps(message)
                client_conn.send(message)
                continue
            d = notes.pop(i)
            print('note has been deleted: ')
            d.printw()
            message = 'ran out of range'
            message = pickle.dumps(message)
            client_conn.send(message)
        elif r[0] == 'sort':
            sort(r[1])
            message = 'notes sorted'
            message = pickle.dumps(message)
            client_conn.send(message)
        pass


if __name__ == '__main__':
    current_port = 10000
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9999))
    server_socket.listen(5)
    print('//---------------server is active---------------//\n    Server log:')
    while True:
        print('waiting for new client...')
        client_socket, client_address = server_socket.accept()
        current_port += 1
        print('new client trying to connect: ', client_address)
        print('redirecting ', client_address, 'to ', current_port, ' port')
        new_port = pickle.dumps(current_port)
        client_socket.send(new_port)
        print('starting new process...')
        p = Process(target=process_task, args=(current_port,))
        p.start()