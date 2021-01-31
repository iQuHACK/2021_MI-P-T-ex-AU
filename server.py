from http import server
import time
import socket
import json

SIZE = 1024
host = "localhost"
port = 8080

sock = socket.socket()
sock.bind(('', port))
sock.listen(2)
conn1, addr1 = sock.accept()
name1 = conn1.recv(SIZE).decode("utf-8")
print('connected:', name1)
conn2, addr2 = sock.accept()
name2 = conn2.recv(SIZE).decode("utf-8")
print('connected:', name2)
conn1.send(name2.encode())
conn2.send(name1.encode())
field1 = conn1.recv(SIZE).decode("utf-8")
turn = name1
conn2.send(turn.encode())
field2 = conn2.recv(SIZE).decode("utf-8")
conn1.send(turn.encode())
while True:
    if (turn == name1):
        shoot = conn1.recv(SIZE).decode("utf-8")
        #shooting processing
        conn1.send(shoot_res_1.encode())
        conn2.send(shoot_res_2.encode())
    else:
        shoot = conn2.recv(SIZE).decode("utf-8")
        #shooting processing
        conn2.send(shoot_res_1.encode())
        conn1.send(shoot_res_2.encode())


conn1.close()
conn2.close()

