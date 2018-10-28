import socket


def switch(tmp):
    i = 0
    while i+1 < len(tmp):
        tmp = tmp[:i] + tmp[i+1] + tmp[i] + tmp[i + 2:]
        i = i + 2
    return tmp


server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind(('localhost', 9090))
print('\nserver is active, waiting for data')

while True:
    string_to_change, client_address = server_sock.recvfrom(1024)
    print('string received: ', string_to_change)
    string_to_send = switch(string_to_change.decode())
    server_sock.sendto(string_to_send.encode(), client_address)
    print('string sent: ', string_to_send)
    print('success')