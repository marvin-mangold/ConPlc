import socket
import time
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.96', 1025))

while True:
    send = input("sendedaten eingeben: ")
    if send == "exit":
        break
    send = send.encode("utf-8")
    clientsocket.send(send)
clientsocket.close()
