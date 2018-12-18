import socket
import _thread

trip1 = ["Warsaw", "bus", "45", "1 month"]
trip2 = ["Egypt", "plane", "70", "15 days"]
trip3 = ["Alps", "mini-bus", "15", "25 days"]
trip4 = ["Hawaii", "plane", "10", "3 weeks"]
trip5 = ["Austria", "boat", "47", "1 month"]
trip6 = ["Belarus", "bus", "34", "12 days"]
trips_array = [trip1, trip2, trip3, trip4, trip5, trip6]


def thread_task(socket, address):
    print("new thread is active")
    while True:
        to_send = ""
        trip_destination = socket.recv(4096)
        if not trip_destination:
            print("client ", address, " disconnected")
            break
        print("Price for sort is  ", trip_destination.decode(), "by ", address)
        for i in range(6):
            if trips_array[i][2] < trip_destination.decode():
                to_send = to_send + trips_array[i][0] + "\n" + "Transport: " + trips_array[i][1] + "\n" + "price is " + trips_array[i][2] + "\n" + "Time in a tour " + trips_array[i][3] + "\n\n"
        if to_send == "":
            to_send = "No matches found"
        socket.send(to_send.encode())


server_address = ('localhost', 9090)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(server_address)
server_socket.listen(5)
clients = 0
print("//-----------server is active-----------//")
while True:
    client_socket, client_address = server_socket.accept()
    print('Connected by ', client_address)
    _thread.start_new_thread(thread_task, (client_socket, client_address))
    clients += 1
    print("Active clients: ", clients)
