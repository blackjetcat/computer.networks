import socket


client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 9090)

while True:
    print('\nto enter program leave the string unfilled')
    string_to_send = input('\nenter the string:')
    if string_to_send == '':
        break
    client_sock.sendto(string_to_send.encode(), server_address)
    print('the string has been sent successfully')
    string_to_print, received_from = client_sock.recvfrom(1024)
    print('new string is: ', string_to_print)
client_sock.close()
print('socket closed')