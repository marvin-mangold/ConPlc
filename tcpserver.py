"""
ConPlc - connect PLC and PC
Copyright (C) 2020  Marvin Mangold (mangold.mangold00@googlemail.com)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import socket
import queue
import threading
import time


class Server(object):
    def __init__(self):
        # connection parameters
        self.ip = "127.0.0.1"  # local ip-address
        self.port = 0  # local port
        self.format = "utf-8"  # format to encode or decode byte data
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.partner = {"id": "", "addr": ""}  # [connection_id, ip-address] of partner
        self.active = False  # server start and stop flag
        self.timeout = False
        self.standby = True
        self.connected = False
        # buffers
        self.buffer_recv = queue.Queue()  # buffer for received data
        self.buffer_send = queue.Queue()  # buffer for data to send
        self.buffer_message = queue.Queue()  # buffer for messages
        # threading parameters
        self.thread = threading.Thread(target=self.run, args=())  # function to be running in thread
        self.thread.daemon = True  # setup thread to end after main programm ends
        self.thread.start()  # start thread

    def run(self):
        # infinite loop
        while True:
            time.sleep(0.001)
            if self.active:
                self.connected = False
                try:
                    if not self.timeout:
                        address = (self.ip, self.port)
                        message = "Server starting".format(ip=self.ip, port=self.port)
                        self.buffer_message.put(["", message])
                        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.connection.bind(address)  # create connection channel
                        message = "Server active: IP ({ip}) Port ({port})".format(ip=self.ip, port=self.port)
                        self.buffer_message.put(["", message])
                        message = "Server listening for connection".format(ip=self.ip, port=self.port)
                        self.buffer_message.put(["", message])
                    self.timeout = False
                    self.connection.settimeout(5)  # turn on listeningtime to check if server is turned off manually----------------------------------
                    self.connection.listen(0)  # wait for partner to connect
                    self.connection.settimeout(None)  # turn off listeningtime-----------------------------------------------------------------------
                    self.partner["id"], self.partner["addr"] = self.connection.accept()  # save partner id and address
                    message = "Server connected to {partner}".format(partner=self.partner["addr"])
                    self.buffer_message.put(["", message])
                    self.connected = True
                    while self.active:  # start datatransfer
                        message = "Server waiting for data"
                        self.buffer_message.put(["", message])
                        try:
                            # Receive Data
                            recv = self.connection.recv(1024)  # waiting for data
                            recv = recv.decode(self.format)  # format recieved data
                            self.buffer_recv.put(recv)
                            # Send Data
                            send = self.buffer_send.get(block=True)  # waiting for data
                            send = send.encode(self.format)  # format send data
                            self.connection.send(send)
                        except WindowsError as errormessage:
                            if "10057" in str(errormessage):
                                message = "Server lost connection to {partner}".format(partner=self.partner["addr"])
                            else:
                                message = errormessage
                            self.buffer_message.put(["", message])
                            break  # break datatransfer, close connection and restart
                        except Exception as errormessage:
                            message = "Servererror {errormessage}".format(errormessage=errormessage)
                            self.buffer_message.put(["", message])
                        break  # break datatransfer, close connection and restart
                    self.connection.close()
                    message = "Server stopped"
                    self.buffer_message.put(["", message])
                except Exception as errormessage:
                    if "timed out" in str(errormessage):
                        self.timeout = True
                        print("timeout")
                    else:
                        message = "Servererror {errormessage}".format(errormessage=errormessage)
                        self.buffer_message.put(["stop", message])
                        self.stop()
            else:
                if not self.standby:
                    message = "Server stopped"
                    self.buffer_message.put(["", message])
                    self.standby = True

    def start(self, ip, port):
        self.ip = ip
        self.port = port
        # set server to active
        self.active = True
        self.standby = False
        self.timeout = False

    def stop(self):
        # set server to inactive
        self.active = False
        self.standby = False
        self.timeout = False
