import socket as sock
import pickle as pck
import _thread as thr


class Trip:
    def __init__(self, trip_name, price, transport, time):
        self.trip_name = trip_name
        self.price = price
        self.transport = transport
        self.time = time


trips = []          # Данные о рейсах
clients_arr = []    # Учёт клиентов
data = []

# Утилити функции для обозначения ключа сортировки
def by_price(trip):
    return trip.price


# Оработка запроса на просмотр
def proc_req_print():
    global trips
    resp = pck.dumps(trips)
    return resp


# Обработка запроса на добавление
def add(note):
    global trips
    trips.append(note)
    print("new note has been added: ", note)
    print("current amount of notes: ", len(trips))
    resp = "note was successfully added"
    resp = pck.dumps(resp)
    return resp


def edit(note, n):
    global trips
    if n >= len(trips):
        resp = 'error! wrong element number'
        resp = pck.dumps(resp)
        return resp
    trips[n] = note
    print('note ', n, " was changed to ", trips[n])
    resp = 'note was successfully edited'
    resp = pck.dumps(resp)
    return resp


def delete(n):
    global trips
    if n >= len(trips):
        resp = 'error! wrong element number'
        resp = pck.dumps(resp)
        return resp
    print('note was deleted: ', trips.pop(n))
    resp = 'note was successfully deleted'
    resp = pck.dumps(resp)
    return resp


def f(cost):
    resp = []
    global data
    for i in data:
        if i.price < cost:
            resp.addpend(i)
    else:
        pass
    resp = pck.dumps(resp)


def sort(s):
    global trips
    global data
    if by_price < s:
        trips = sorted(trips, key=by_price)
    resp = 'success'
    resp = pck.dumps(resp)
    return resp


def client_handler(client, address, t_id):
    print("new thread is active, id: ", t_id)
    while True:
        request = client.recv(1024)
        if not request:
            break
        request = pck.loads(request)
        print("new request from ", address, ": ", request[0])
        #
        if request[0] == 'print':
            resp = proc_req_print()
            client_socket.send(resp)
        elif request[0] == 'add':
            resp = add(request[1])
            client_socket.send(resp)
        elif request[0] == 'edit':
            resp = edit(request[1], request[2])
            client_socket.send(resp)
        elif request[0] == 'del':
            resp = delete(request[1])
            client_socket.send(resp)
        elif request[0] == 'sort':
            resp = sort(request[1])
            client_socket.send(resp)

        print("response to ", address, "request ", request[0], " was sent")
    print("client ", address, " disconnected")
    clients_arr.pop(t_id)
    print("active clients ", len(clients_arr))


server_address = ("localhost", 7070)
server_socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(3)
print("//------------server is active!------------//\n    server log:")
# Подключение новых клиентов
while True:
    client_socket, client_address = server_socket.accept()
    print("new client connected: ", client_address)
    message = pck.dumps("connected")
    client_socket.send(message)
    thr.start_new_thread(client_handler, (client_socket, client_address, len(clients_arr)))
    clients_arr.append((client_socket, client_address))     # Учёт автивных клиентов
    print("active clients: ", len(clients_arr))