import socket
import pickle
import datetime
import _thread as thread
import DBhandler


def pt():
    d = datetime.datetime.now().time()
    h = str(d.hour)
    if len(h) == 1:
        h = '0' + h
    m = str(d.minute)
    if len(m) == 1:
        m = '0' + m
    t = h + ':' + m
    return t


def sqlreq(conn, flag, args):
    print(pt(), 'запрос на просмотр сообщений от пользователя ', args[0])
    msgs = DBhandler.pull_messages(conn, flag, args[0], args[1], args[2])
    if not msgs:
        return False
    print(pt(), 'Список сообщений был отправлен пользователю ', args[0])
    return msgs


def sign(conn, db_conn, db_file):
    while True:
        sign = conn.recv(1024)
        sign = pickle.loads(sign)
        if sign[0] == 'up':
            # Попытка добавления нового пользователя
            print(pt(),  'Запрос на регистрацию')
            r_id = DBhandler.add_user(db_conn, sign[1], sign[2])
            if not r_id:
                # Сообщение об ошибке
                resp = (False, 'Такой пользователь уже существует!')
                resp = pickle.dumps(resp)
                conn.send(resp)
                print(pt(), 'Запрос на регистрацию был отменён')
                continue
            resp = (True, 'Пользователь зарегистрирован')
            resp = pickle.dumps(resp)
            conn.send(resp)
            break
        elif sign[0] == 'in':
            # Попытка залогиниться
            print(pt(),  'Запрос на авторизацию')
            cur_id = DBhandler.check_user(db_conn, sign[1], sign[2])
            if not cur_id:
                resp = (False, 'Неправильный логин и/или пароль!')
                resp = pickle.dumps(resp)
                conn.send(resp)
                print(pt(), ' Запрос на авторизацию был отменён')
                continue
            resp = (True, 'Вход в систему завершён успешно')
            resp = pickle.dumps(resp)
            conn.send(resp)
            print(pt(), 'Пользователь авторизирован')
            break


def client_handler(conn, addr, db_file):
    sql = DBhandler.open_db(db_file)
    print(pt(), 'Новый поток создан')
    # Вход/регистрация
    try:
        sign(conn, sql, db_file)
    except:
        print(pt(), 'Клиент принудительно разорвал соединение')
        sql.close()
        print(pt(), 'Поток уничтожен')
        return
    while True:
        req = conn.recv(2048)
        if not req:
            print(pt(), 'Клиент отключился')
            break
        req = pickle.loads(req)
        if req[0] == 'send':
            DBhandler.add_message(sql, req[1])
        elif req[0] == 'view':
            res = sqlreq(sql, req[1], req[2])
            if not res:
                resp = False
                resp = pickle.dumps(resp)
                conn.send(resp)
            resp = pickle.dumps(res)
            conn.send(resp)
        elif req[0] == 'del':
            print(pt(), 'Поступил запрос на удаление последнего сообщения от', req[1])
            DBhandler.del_last(sql, req[1])
    print(pt(), 'Поток уничтожен')
    sql.close()


db_name = 'database/server.db'
ADDR = ('localhost', 9000)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(10)
# Открытие  БД
tmp = DBhandler.open_db('database/server.db')
tmp.close()
print('//---------------Сервер активен---------------//')
# Подключение новых полльзователей
while True:
    client_conn, client_addr = server_socket.accept()
    print(pt(), 'Запрос на новое подключение от ', client_addr)
    thread.start_new_thread(client_handler, (client_conn, client_addr, db_name))