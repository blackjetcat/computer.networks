import _socket as sock
import _pickle as pck
import requests as req


# Ренейминг функций, которые я зачем-то так сложно назвал
r_print = req.form_req_print    # Просмотр записей
r_edit = req.form_req_edit      # Редактирование записи
r_add = req.form_req_add        # Добавление записи
r_del = req.form_req_del        # Удаление
view = req.view                 # Прилетели данные, которые надо вывести
sort = req.form_req_sort      # Сортировка

server_address = ("localhost", 7070)
client_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
print("connecting to the server...")
client_socket.connect(server_address)
message = client_socket.recv(1024)
message = pck.loads(message)
print(message)
while True:
    print("enter a number of command or /'command'")
    print("1. print\n2. edit\n3. add\n4. delete\n5. sort\n0. exit")
    switch = input("input> ")
    if switch == "1" or switch == "/print":
        request = r_print()
        client_socket.send(request)
        data = client_socket.recv(1024)
        data = pck.loads(data)
        if len(data) == 0:
            print("no notes")
            continue
        view(data)
        continue
    elif switch == '2' or switch == "/edit":
        request = r_edit()
        client_socket.send(request)
    elif switch == '3' or switch == "/add":
        request = r_add()
        client_socket.send(request)
    elif switch == '4' or switch == "/delete":
        request = r_del()
        client_socket.send(request)
    elif switch == '5' or switch == "/sort":
        request = sort()
        client_socket.send(request)
    elif switch == '0' or switch == "/exit":
        break
    else:
        print("input error, try again")
        continue
    message = client_socket.recv(1024)
    message = pck.loads(message)
    print(message)
print("disconnecting")
client_socket.close()