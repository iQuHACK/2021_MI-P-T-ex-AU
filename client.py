import socket
import json

SIZE = 1024
print("Choose your Name:")
name = input()
#host = "54.197.50.9"
host = "127.0.0.1"
port = 8080
sock = socket.socket()
sock.connect((host, port))
sock.send(name.encode())
print("Waiting for another Player...")
opponent = sock.recv(SIZE).decode("utf-8")
print(opponent, "connected")

#setting up your battlefield 
field = "test"
sock.send(field.encode())
turn = (sock.recv(SIZE).decode("utf-8")==name)
while True:
	if(turn):
		#shooting
		sock.send(shoot.encode())
		shoot_result = sock.recv(SIZE).decode("utf-8")
		#drawing your shoot result & changing turn 

	else: 
		enemy_shoot = sock.recv(SIZE).decode("utf-8")
		#drawing result of enemy shoot & changing turn 

	if (winner):
		break

#drawing winner 

sock.close()
