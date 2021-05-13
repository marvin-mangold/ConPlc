"""
ConPlc - connect PLC and PC
Copyright (C) 2021  Marvin Mangold (Marvin.Mangold00@googlemail.com)

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
        """
        setup connection parameters
        setup buffers
        setup thread
        """
        # connection parameters
        self.ip = "127.0.0.1"  # local ip-address
        self.port = 0  # local port
        self.encode_decode = False  # recv/send bytes should be en/decoded?
        self.format = "utf-8"  # format to en/decode recv/send bytes
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.active = False  # server start and stop flag
        self.timeout = False  # flag to restart waiting for connections
        self.connected = False  # flat to indicate if connection is established
        self.partner_ip = ""  # ip-address of connected partner
        self.partner_id = None  # connection id to receive and end data
        self.datasize = 0  # number of bytes to collect while receiving
        self.buffer_package = []  # bytes from the received packages
        # buffers
        self.buffer_recv = queue.Queue()  # buffer for received data
        self.buffer_send = queue.Queue()  # buffer for data to send
        self.buffer_message = queue.Queue()  # buffer for messages
        # threading parameters
        self.thread = threading.Thread(target=self.run, args=())  # function to be running in thread
        self.thread.daemon = True  # setup thread to end after main programm ends
        self.thread.start()  # start thread

    def run(self):
        """
        connect to partner
        receive data
        send data
        """
        while True:  # infinite loop
            time.sleep(0.001)
            while self.active and not self.connected:  # start connecting
                try:  # try to open socket and connect to requesting partner
                    if not self.timeout:  # messages are muted when timeout occurred
                        self.message("", "Server starting".format(ip=self.ip, port=self.port))
                    self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.connection.bind((self.ip, self.port))  # create connection channel
                    if not self.timeout:  # messages are muted when timeout occurred
                        self.message("", "Server active @ IP ({ip}) Port ({port})".format(ip=self.ip, port=self.port))
                        self.message("", "Server listening for connection".format(ip=self.ip, port=self.port))
                    self.connection.listen(0)  # wait for partner to connect
                    self.connection.settimeout(1)  # turn on listeningtime to check if server is turned off manually
                    self.partner_id, self.partner_ip = self.connection.accept()  # save partner id and address
                    self.message("", "Server connected to {partner}".format(partner=self.partner_ip))
                except Exception as errormessage:  # an error occurred
                    if "timed out" in str(errormessage):  # if error = timeout --> retry connecting with muted messages
                        self.timeout = True
                    else:
                        self.timeout = False
                        self.message("stop", "Servererror {errormessage}".format(errormessage=errormessage))
                        self.connection.close()
                        self.connected = False
                        self.active = False
                        break
                else:  # connection established start datatransfer
                    self.timeout = False
                    self.message("", "Server waiting for data")
                    self.connected = True

            while self.active and self.connected:  # start datatransfer

                try:  # try to receive data
                    self.partner_id.settimeout(1)  # turn on listeningtime to check if server is turned off manually
                    recv = self.partner_id.recv(1000)  # waiting for maximal 1000 bytes data
                except Exception as errormessage:  # an error occurred
                    if "timed out" in str(errormessage):  # if error = timeout --> retry receiving data
                        self.timeout = True
                    else:  # break datatransfer, close connection and restart
                        self.timeout = False
                        self.message("", str(errormessage))
                        self.connection.close()
                        self.connected = False
                        break
                else:  # data received
                    self.timeout = False
                    if self.encode_decode:  # if activated the data will be  decoded
                        recv = recv.decode(self.format, 'ignore')  # format received data
                    if not recv:  # if no data in received data, partner closed connection
                        self.message("", "Server lost connection to {partner}".format(partner=self.partner_ip))
                        self.connection.close()
                        self.connected = False
                        break
                    else:
                        self.buffer_package += recv  # save received data in package buffer
                        # print("Server received {x}/{y} bytes".format(x=len(self.buffer_package), y=self.datasize))
                        # check if all bytes (defined by self.datasize) are collected
                        if len(self.buffer_package) >= self.datasize:
                            # if more bytes in package buffer than expected put the expected bytes in receive buffer
                            # save the leftover bytes for the next receiving
                            newdata = self.buffer_package[:self.datasize]  # = expected size of bytes
                            nextdata = self.buffer_package[self.datasize:]  # > expected size of bytes
                            self.buffer_recv.put(newdata)  # put received data in buffer
                            self.buffer_package = nextdata  # save the leftover bytes
                            # send answer to partner
                            send = self.buffer_send.get(block=True)  # waiting for data in buffer
                            if self.encode_decode:  # if activated the data will be  encoded
                                send = send.encode(self.format, 'ignore')  # format send data
                            try:  # try to send data
                                self.partner_id.send(send)
                            except Exception as errormessage:  # an error occurred
                                # break datatransfer, close connection and restart
                                self.message("", str(errormessage))
                                self.connection.close()
                                self.connected = False
                                break
                        # not all bytes received keep on receiving
                        else:
                            self.timeout = False

    def start(self, ip, port, datasize):
        """
        start communication
        """
        self.ip = ip
        self.port = port
        self.datasize = datasize
        # set server to active
        self.active = True
        self.timeout = False

    def stop(self):
        """
        stop communication
        """
        # set server to inactive
        self.active = False
        self.timeout = False
        self.message("", "Server stopped")

    def message(self, cmd, message):
        """
        put message to buffer
        """
        self.buffer_message.put([cmd, message])
