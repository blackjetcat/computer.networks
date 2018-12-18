"""
Модуль с процедурами для управление БД
SQL запросы
"""
import _sqlite3 as sqlite
import datetime
import messages


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


"""**********************---Запросы для таблицы с пользователями---**************************"""


# инициализация БД
def init_db(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE users (user_id int, login text, password text)''')
    c.execute('''CREATE unique index ulogin on  users(login)''')
    c.execute('''CREATE TABLE messages (date datetime, owner int, sender text, receiver text, message text)''')
    conn.commit()
    print(pt(), ' База данных была успешно создана')


# Открытие БД
def open_db(file):
    conn = sqlite.connect(file)
    c = conn.cursor()
    try:
        c.execute('''SELECT * FROM users''')
    except:
        print(pt(), 'Не удалось открыть файл базы данных')
        init_db(conn)
    return conn


# Добавление нового пользователя
def add_user(conn, login, password):
    c = conn.cursor()
    c.execute('''SELECT MAX(user_id) FROM users''')
    res = c.fetchone()
    if res[0] == None:
        curr_id = 0
    else:
        curr_id = res[0]
    try:
        c.execute('''INSERT INTO users VALUES(?, ?, ?)''', (curr_id + 1, login, password))
        c.execute('''SELECT MAX(user_id) FROM users''')
    except:
        print(pt(), 'Попытка регистрации существующего пользователся')
        return False
    new_id = c.fetchone()[0]
    print(pt(), 'Уникальный id нового польователя: ', new_id)
    conn.commit()
    return new_id


# Проверка на существующего пользователя
def check_user(conn, login, password):
    c = conn.cursor()
    c.execute('''SELECT user_id FROM users WHERE login = ? and password = ?''', (login, password))
    res = c.fetchone()
    if res == None:
        return False
    else:
        return res[0]


"""*************************---Запросы для таблицы с пользователями---**************************"""


def add_message(conn, msg):
    c = conn.cursor()
    c.execute('''INSERT INTO messages VALUES (?, ?, ?, ?, ?)''',
              (msg.date, msg.owner, msg.sender, msg.receiver, msg.message))
    print(pt(), 'сообщение добавлено в таблицу')
    conn.commit()


def pull_messages(conn, flag, receiver, sender, msg):
    msg = '%' + msg + '%'
    c = conn.cursor()
    if flag == 'in':
        if sender == '':
            sqltext = 'SELECT * FROM messages WHERE (sender = ? OR receiver = ?)'
        else:
            sqltext = 'SELECT * FROM messages WHERE (sender = ? AND receiver = ?)'
    elif flag == 'out':
        if receiver == '':
            sqltext = 'SELECT * FROM messages WHERE (sender = ? OR receiver = ?)'
        else:
            sqltext = 'SELECT * FROM messages WHERE (sender = ? AND receiver = ?)'
    elif flag == 'all':
        sqltext = 'SELECT * FROM messages WHERE (sender = ? OR receiver = ?)'
    try:
        sqltext += 'AND message LIKE ?'
        c.execute(sqltext, (sender, receiver, msg))
    except:
        print(pt(), 'Сообщения не найдены')
        return False
    res = c.fetchall()
    return res


def del_last(conn, login):
    c = conn.cursor()
    sqltext = 'delete from messages where receiver = ?'
    c.execute(sqltext, (login))
    print(pt(), 'Последнее псиьмо польователя', login, 'было удалено')
    conn.commit()