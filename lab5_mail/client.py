import socket
import pickle
import time
import messages


def del_last(conn, login):
    req = ('del', login)
    req = pickle.dumps(req)
    conn.send(req)


def view(conn, login):
    sender = ''
    msg = ''
    while True:
        print('\nЧтобы пропустить значение,оставьте строку пустой')
        print('1) Входящие || 2) Исходящие || 3) Все')
        i = input('Ввод: ')
        if i == '1':
            receiver = login
            sender = input('От кого: ')
            msg = input('Ключевые слова: ')
            f = 'in'
            break
        elif i == '2':
            sender = login
            receiver = input('Кому: ')
            msg = input('Ключевые слова: ')
            f = 'out'
            break
        elif i == '3':
            msg = input('Ключевые слова: ')
            sender = login
            receiver = login
            f = 'all'
            break
        else:
            print('Ошибка ввода! Попробуйте ещё раз')
    args = (receiver, sender, msg)
    req = ('view', f, args)
    req = pickle.dumps(req)
    conn.send(req)
    pull = conn.recv(4096)
    pull = pickle.loads(pull)
    try:
        messages.print_messages(pull, login)
    except:
        print('Сообщения не найдены')


def view_messages(conn, login):
    print('Чтобы оставить параметр пустым, оставьте строку пустокй')
    fr = input('Чьи сообщения вывести: ')
    if fr == '':
        fr = None
    msgs = input('Ключевые фразы в сообщениях: ')
    args = (login, fr, msgs)
    req = ('view', args)
    req = pickle.dumps(req)
    conn.send(req)
    resp = conn.recv(4096)
    if not resp:
        print('Таких сообщений не найдено')
        return False
    resp = pickle.loads(resp)
    messages.print_messages(resp, login)


def send_message(conn, login):
    receiver = input('Имя получателя: ')
    message = input('Введите ваше сообщение:\n')
    sender = login
    d = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = messages.Message(d, sender, receiver, message)
    msg = pickle.dumps(('send', msg))
    conn.send(msg)
    print('Сообщение было отправлено')


def sign_in(conn):
    while True:
        login = input('Введите логин: ')
        password = input('Вветиде пароль: ')
        send = ('in', login, password)
        send = pickle.dumps(send)
        conn.send(send)
        sysmsg = conn.recv(1024)
        sysmsg = pickle.loads(sysmsg)
        print(sysmsg[1])
        if sysmsg[0]:
            return login, password


def sign_up(conn):
    while True:
        login = input('Логин: ')
        password = input('Пароль: ')
        send = ('up', login, password)
        send = pickle.dumps(send)
        conn.send(send)
        sysmsg = conn.recv(1024)
        sysmsg = pickle.loads(sysmsg)
        print(sysmsg[1])
        if sysmsg[0]:
            return login, password


ADDR = ('localhost', 9000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Попытка подключения к серверу...')
client_socket.connect(ADDR)
print('Подключено')
while True:
    print('1) Войти || 2) Зарегистрироваться')
    i = input('Ввод: ')
    if i == '1':
        log, pas = sign_in(client_socket)
        break
    elif i == '2':
        log, pas = sign_up(client_socket)
        break
    else:
        print('Ошибка ввода! попробуйте ещё раз')
while True:
    print('1) Отправить сообщение\n2) Просмотреть сообщения')
    print('3) Удалить последнее\n0) Выйти')
    i = input('Ввод: ')
    if i == '1':
        send_message(client_socket, log)
    elif i == '2':
        view(client_socket, log)
    elif i == '3':
        del_last(client_socket, log)
    elif i == '0':
        break
    else:
        print('Ошибка ввода! Попробуйте ещё раз')