import logging
import socket
import json

import constCS
import lab_logging

lab_logging.setup()  # init loging channels for the lab


class Server:
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Server")

    tel = {'natalia': '1234', 'alice': '8765', 'jana': '2921', 'hendrik': '1801'}

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents errors due to "addresses in use"
        self.sock.bind((constCS.HOST, constCS.PORT))
        self.logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        self.sock.listen(1)
        self.logger.info("Server is listening for client")

        (connection, address) = self.sock.accept()  # returns new socket and address of client
        
        while True:  # forever
            data = connection.recv(1024).decode('ascii')  # receive data from client

            # print ("Erhaltener command:" + data.decode('ascii'))
            if not data:
                # TCP-Connection lost
                self.logger.info("Server didn´t get data")
                break

            self.logger.info("Server got some data: " + data)            
            # Send all
            if data == 'getAll':
                teljson = json.dumps(self.tel)
                #for key, value in self.tel.items():
                print(teljson)
                connection.send(teljson.encode('ascii'))
                self.logger.info("Server sent data: " + teljson)
                break

            # Send single name 
            if data in self.tel:   
                connection.send((data + ' - ' + self.tel[data]).encode('ascii'))
                self.logger.info("Server sent data: " + self.tel[data])
                break

            # Send data not found
            else:
                connection.send(('No data found for ' + data).encode('ascii'))
                break
            
        connection.close()  # close the connection
        self.sock.close()
        self.logger.info("Server closed connection.")


class Client:
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constCS.HOST, constCS.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

    def call(self, msg_in="Hello, world"):
        self.sock.send(msg_in.encode('ascii'))  # send encoded string as data
        data = self.sock.recv(1024)  # receive the response
        msg_out = data.decode('ascii')
        print(msg_out)  # print the result
        self.sock.close()  # close the connection
        self.logger.info("Client down.")
        return msg_out

    def get(self, name):
        self.sock.send(name.encode('ascii')) # send name as string
        self.logger.info("Client sent name: " + name)

        data = self.sock.recv(1024)  # receive the response
        self.logger.info("Client got response: " + data.decode('ascii'))

        number = data.decode('ascii')
        self.sock.close()  # close the connection
        self.logger.info("Client closed connection.")
        return number

    def getAll(self):
        self.sock.send('getAll'.encode('ascii')) # send name as string
        self.logger.info("Client sent getAll")

        data = self.sock.recv(1024)  # receive the respone
        output = data.decode('ascii')
        self.logger.info("Client got response: " + output)

        dataToArray = json.loads(data)
        for key, value in dataToArray.items():
           print(key + ' ' + value + ';')
        self.sock.close()  # close the connection
        self.logger.info("Client closed connection.")
        return dataToArray