import socket
import pickle


def check(data):
    if data[0]<data[4]<data[2] and data[1]<data[5]<data[3]:
        return True
    else:
	    return False


HOST = '127.0.0.1'
PORT = 53210
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
print('\nServer is active\n')
conn, addr = s.accept()
print( 'Connected by', addr)
while 1:
    data = conn.recv(4096)
    if not data: break
    data = pickle.loads(data)
    print('Data recieved ',data)
    if check(data):
        to_send = 'Yes, recieved point IS in rectangle'
    else:
        to_send = 'No, recieved point ISN"T in rectangle'

    conn.send(to_send.encode())
    print('result has been sent successfully')
conn.close()