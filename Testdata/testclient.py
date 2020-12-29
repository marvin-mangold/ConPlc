import socket
import time
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.96', 1024))
time.sleep(10)
clientsocket.close()
