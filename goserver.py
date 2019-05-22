import socket
import os


def main():
    server()

def server():
    host = socket.gethostname()   # get local machine name
    port = 6666  # Make sure it's within the > 1024 $$ <65535 range

    s = socket.socket()
    s.bind(("", port))
    print(s)

    s.listen(1)

    while True:
        client_socket, addr = s.accept()
        c = client_socket
        print('Got connection from', addr)
        data = c.recv(1024)
        print('Server received', repr(data))

        name = '/mys3bucket' + data.decode('utf-8')

        os.system(f"cd darknet-master && ./darknet detect cfg/yolov3.cfg yolov3.weights {name} >/mys3bucket/robots/res.txt")

        data = open('/mys3bucket/robots/res.txt', 'rb').read()
        print('answer sent')
        c.send(data)
        c.close()



if __name__ == '__main__':
    main()
