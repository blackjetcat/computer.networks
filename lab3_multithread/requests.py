import pickle


# Класс с поездо4ками
class Trip:
    def __init__(self, trip_name, price, transport, time):
        self.trip_name = trip_name
        self.price = price
        self.transport = transport
        self.time = time


def view(data):
    for i in range(len(data)):
        print("\ntrip number: ", data[i].trip_name)
        print("   price: ", data[i].price)
        print("      transport: ", data[i].transport)
        print("time: ", data[i].time
)


"""************************************
Формирование запросов клиента
************************************"""


# Формирование запроса на просмотр элементов
def form_req_print():
    request = ('print',)
    request = pickle.dumps(request)
    return request


# Формирования запроса на добавление элемента
def form_req_add():
    trip_number = input("trip name: ")
    price = input("price: ")
    transport = input("transport: ")
    time = input("time: ")
    note = Trip(trip_number, price, transport, time)
    request = ("add", note)
    request = pickle.dumps(request)
    return request


# Формирование запроса на изменение записи
def form_req_edit():
    n = input("choose note to edit: ")
    trip_number = input("trip number: ")
    price = input("price: ")
    transport = input("transport: ")
    time = input("time: ")
    note = Trip(trip_number, price, transport, time)
    request = ("edit", note, int(n))
    request = pickle.dumps(request)
    return request


# Формирование запроса на удаление эелемента
def form_req_del():
    to_del = input("number of element to del: ")
    request = ('del', int(to_del))
    request = pickle.dumps(request)
    return request


def form_req_sort():
    print("\nsort by: ")
    print("1. price\n2. transport\n3. time")
    sort = input("input> ")
    request = ('sort', sort)
    request = pickle.dumps(request)
    return request
