import socket
import pickle

HOST = '127.0.0.1'
PORT = 53210
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print('Input x1')
x1 = input()
print('Input y1')
y1 = input()
print('Input x2')
x2 = input()
print('Input y2')
y2 = input()
print('Input x of your point')
xp = input()
print('Input y of your point')
yp = input()

arr = ([x1,y1,x2,y2,xp,yp])
data_string = pickle.dumps(arr)
s.send(data_string)

answer = s.recv(4096)
print(answer)
s.close()