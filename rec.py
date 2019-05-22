import os
import socket 

path_to_audio =  '/Users/alinacodzy/Downloads/big_1576456.jpg'
another_path = '/home/robotis/Desktop/mega_team/2.ogg'

def conn():
	sock = socket.socket()
	sock.connect(('18.222.114.115', 8080))
	return sock


def send_audio(sock, path_to_audio):
	f = open(path_to_audio, 'rb')
	l = f.read()
	lenght = len(l)
	print(lenght)
	sock.send(str(lenght))
	f.close() # sent lenght
	
	f = open(path_to_audio, 'rb')
	l = f.read(1024)
	while (l):
		sock.send(l)
		l = f.read(1024)
	f.close() #  sent audio file


def recv_audio(sock, another_path):
	f = open(another_path, 'wb')
	remaining = sock.recv(1024)
	

	remaining = int(remaining)
	while remaining:
		rbuf = sock.recv(min(remaining, 1024))
		remaining -= len(rbuf)
		f.write(rbuf)
	f.close()


sock = conn()
if sock == None:
	print('Not today')
while True:
	print("I am recording%%%%%%%%%%%")
	os.system("arecord -D hw:1,0 -f S16_LE -d 7 /home/robotis/Desktop/mega_team/1.ogg")
	send_audio(sock, path_to_audio)
	recv_audio(sock, another_path)
	os.system("play /home/robotis/Desktop/mega_team/2.ogg")
