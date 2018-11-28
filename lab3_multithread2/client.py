import socket

server_address = ('localhost', 9090)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
print("connected to ", server_address)
# Working cycle
while True:
    print("to exit leave the string unfilled")
    to_send = input("Enter price: ")
    if to_send == "":
        client_socket.close()
        break
    client_socket.send(to_send.encode())
    to_print = client_socket.recv(1024)
    print("Result found:\n ", to_print.decode())
