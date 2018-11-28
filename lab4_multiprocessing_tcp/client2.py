import socket
import pickle
import requests


# Создаём начальный сокет
server_address = ('localhost', 9999)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('connecting to server...')
client_socket.connect(server_address)
# Получаем адрес сокета из нового процесса
new_address = client_socket.recv(1024)
new_address = pickle.loads(new_address)
# Закрываем сокет, предварительно получив адрес
own_address = client_socket.getsockname()
client_socket.close()
# Создаём сокет для подключения к сокету в новом прцоессе
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(own_address)
print('redirecting to ', new_address, ' host...')
client_socket.connect(('localhost', new_address))
while True:
    print('\nenter number of command or /"command"')
    print('1.  print\n2.    add\n3.   edit\n4. delete\n5.   sort\n0.   exit')
    i = input('input> ')
    if i == '0' or i == '/exit':
        break
    elif i == '1' or i == '/print':
        r = requests.print_request()
        client_socket.send(r)
        data = client_socket.recv(1024)
        data = pickle.loads(data)
        requests.print_data(data)
    elif i == '2' or i == '/add':
        r = requests.add_request()
        client_socket.send(r)
        message = client_socket.recv(1024)
        print(pickle.loads(message))
    elif i == '3' or i == '/edit':
        r = requests.edit_request()
        if not r:
            continue
        r = pickle.dumps(r)
        client_socket.send(r)
        message = client_socket.recv(1024)
        print(pickle.loads(message))
    elif i == '4' or i == '/delete' or i == '/del':
        r = requests.delete_request()
        client_socket.send(r)
        message = client_socket.recv(1024)
        print(pickle.loads(message))
    elif i == '5' or i == '/sort':
        r = requests.sort_request()
        if not r:
            continue
        client_socket.send(r)
        message = client_socket.recv(1024)
        print(pickle.loads(message))
    else:
        print('input error! try again')
client_socket.close()
print('socket closed')